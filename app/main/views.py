from flask import render_template, request, redirect, url_for, flash
from werkzeug import secure_filename
from flask_login import current_user
from flask import current_app
import os
from . import main
from ..models import Category, Application, Developer, ApplicationAssets, User
from .. import db
from .forms import ApplicationsForm, CategoryForm, ApplicationAssetsForm

ALLOWED_EXTENSIONS = set(
    ['sh', 'jpg', 'png', 'jpeg', 'svg', 'mp4', 'flv', 'mkv', '3gp']
)


def populate_categories(form):
    """
    Pulls choices from the database to populate our select fields.
    """
    categories = Category.query.all()
    category_names = {'0': 'Choose Category'}

    for category in categories:
        category_names[category.id] = category.name

    category_choices = [(k, v) for k, v in category_names.iteritems()]
    form.category_id.choices = category_choices


def populate_developers(form):
    """
    Pulls choices from the database to populate our select fields.
    """
    developers = Developer.query.all()
    developer_names = {'0': 'Choose Developer'}

    for developer in developers:
        developer_names[developer.user_id] = developer.name

    developer_choices = [(k, v) for k, v in developer_names.iteritems()]
    form.developer_id.choices = developer_choices


def allowed_file(filename):
    """
    Checks whether a given file extension is allowed.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def load_applications(**kwargs):
    """
    Populate applications from database based on parameters passed
    """
    applications = []

    apps = None

    if 'app_id' in kwargs and 'category_id' not in kwargs:
        apps = Application.query.filter_by(id=kwargs['app_id']).all()
    elif 'category_id' in kwargs and 'app_id' in kwargs:
        apps = Application.query.filter_by(category_id=kwargs['category_id'])\
                                .filter(Application.id != kwargs['app_id']).all()
    elif 'category_id' in kwargs and 'app_id' not in kwargs:
        apps = Application.query.filter_by(category_id=kwargs['category_id']).all()
    else:
        apps = Application.query.all()

    for app in apps:
        assets = ApplicationAssets.query.filter_by(application_id=app.id).first()
        developer = Developer.query.filter_by(user_id=app.developer_id).first()

        app_details = {
            'id': app.id,
            'name': app.name,
            'developer': developer.name,
            'icon': assets.icon,
            'description': app.description,
            'downloads': app.downloads
        }

        applications.append(app_details)

    return applications


@main.route('/')
def index():
    user = User.query.filter_by(id=current_user.id).first()
    installed_apps = []
    for app in get_installed_apps(user):
        installed_apps.append(load_applications(app_id=app))

    for app in installed_apps:
        print 'installed_app =>', app[0]

    applications = load_applications()
    for app in range(len(applications)):
        if applications[app]['id'] in get_installed_apps(user):
            applications.pop(app)

    return render_template('index.html',
                           applications=applications,
                           installed_apps=installed_apps)


@main.route('/app_assets/<int:app_id>', methods=['GET', 'POST'])
def app_assets(app_id):
    application = Application.query.filter_by(id=app_id).first()
    developer = Developer.query.filter_by(user_id=application.developer_id).first()

    form = ApplicationAssetsForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            APP_DIR = os.path.abspath(os.path.join(__file__, "../.."))
            INSTALLS_DIR = os.path.join(APP_DIR, current_app.config['UPLOAD_FOLDER'])
            ASSETS_DIR = os.path.join(INSTALLS_DIR, str(app_id))

            if not os.path.exists(ASSETS_DIR):
                os.makedirs(ASSETS_DIR)

            app_assets = {}

            for field in form:
                if field.type == "FileField":
                    field_name = field.name
                    field_data = field.data

                    if field_data.filename == '':
                        flash('No selected file', 'error')
                        return redirect(request.url)

                    if field_data and allowed_file(field_data.filename):
                        asset_name = secure_filename(field_data.filename)
                        file_ext = asset_name.rsplit('.', 1)[1]
                        new_asset_name = field_name + '.' + file_ext
                        app_assets[field_name] = new_asset_name

                        field_data.save(os.path.join(ASSETS_DIR, asset_name))

                        file_dir = os.path.join(ASSETS_DIR, asset_name)
                        new_file_dir = os.path.join(ASSETS_DIR, new_asset_name)
                        print 'old file =>', file_dir
                        print 'new file =>', new_file_dir
                        os.rename(file_dir, new_file_dir)

            assets = ApplicationAssets(
                application_id=app_id,
                icon=app_assets.get('icon', 'app_icon.png'),
                screenShotOne=app_assets.get('screenshot1', 'browser.png'),
                screenShotTwo=app_assets.get('screenshot2', 'browser.png'),
                screenShotThree=app_assets.get('screenshot3', 'browser.png'),
                screenShotFour=app_assets.get('screenshot4', 'browser.png'),
                video=app_assets.get('video', 'None'))

            db.session.add(assets)
            db.session.commit()

            flash('Assets added successfully', 'success')
        return redirect(request.args.get('next') or url_for('main.app_info', app_id=app_id))

    return render_template('app_assets.html', form=form, application=application, developer=developer)


@main.route('/app_info/<int:app_id>')
def app_info(app_id):
    application = Application.query.filter_by(id=app_id).first()
    developer = Developer.query.filter_by(user_id=application.developer_id).first()
    assets = ApplicationAssets.query.filter_by(application_id=app_id).first()

    app_details = load_applications(app_id=app_id)
    related_apps = load_applications(category_id=application.category_id, app_id=app_id)

    return render_template('app_info.html', app_details=app_details, related_apps=related_apps, assets=assets)


@main.route('/install_app')
def install_app():
    user_id = request.args['user_id']
    app_id = request.args['app_id']

    user = User.query.filter_by(id=user_id).first()
    app = Application.query.filter_by(id=app_id).first()

    try:
        user.installed_apps.append(app)
        db.session.commit()

        flash('Application installed successfully', 'success')
    except Exception as e:
        db.session.rollback()
        db.session.flush()

        flash('Application did not install successfully', 'error')

    return redirect(url_for('main.index'))


def get_installed_apps(user):
    return [app.id for app in user.installed_apps]


@main.route('/application', methods=['GET', 'POST'])
def application():
    form = ApplicationsForm()
    populate_categories(form)
    populate_developers(form)

    if request.method == 'POST':
        if form.validate_on_submit():
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part', 'error')
                return render_template('application.html', form=form)
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file', 'error')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                APP_DIR = os.path.abspath(os.path.join(__file__, "../.."))
                INSTALLS_DIR = os.path.join(APP_DIR, current_app.config['UPLOAD_FOLDER'])
                filename = secure_filename(file.filename)
                FILE_PATH = os.path.join(INSTALLS_DIR, filename)
                file.save(os.path.join(INSTALLS_DIR, filename))

                size = os.stat(FILE_PATH).st_size
                app_name = filename.rsplit('.', 1)[0]

                application = Application(
                    category_id=form.category_id.data,
                    developer_id=form.developer_id.data,
                    name=app_name,
                    version=form.version.data,
                    description=form.description.data,
                    size=size,
                    permission=form.permission.data,
                    osVersion=form.osVersion.data,
                    launchurl=form.launchurl.data)

                db.session.add(application)
                db.session.commit()

            flash('Application added successfully', 'success')
        return redirect(request.args.get('next') or url_for('main.application'))

    return render_template('application.html', form=form)


@main.route('/category', methods=['GET', 'POST'])
def category():
    form = CategoryForm()
    categories = Category.query.all()

    if request.method == 'POST':
        if form.validate_on_submit():
            category = Category(name=form.name.data,
                                description=form.description.data)
            db.session.add(category)
            db.session.commit()

            flash('Category added successfully', 'success')
        return redirect(request.args.get('next') or url_for('main.category'))

    return render_template('category.html', form=form, categories=categories)
