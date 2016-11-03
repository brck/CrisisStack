from flask import render_template, request, redirect, url_for, flash
from werkzeug import secure_filename
from flask import current_app
import os
from . import main
from ..models import Category, Application, Developer, ApplicationAssets
from .. import db
from .forms import ApplicationsForm, CategoryForm, ApplicationAssetsForm

ALLOWED_EXTENSIONS = set(['sh', 'jpg', 'png', 'jpeg', 'svg', 'mp4', 'flv', 'mkv', '3gp'])


def populate_categories(form):
    """
    Pulls choices from the database to populate our select fields.
    """
    categories = Category.query.all()
    category_names = {'0':'Choose Category'}

    for category in categories:
        category_names[category.id] = category.name

    category_choices = [(k, v) for k, v in category_names.iteritems()]
    form.category_id.choices = category_choices


def populate_developers(form):
    """
    Pulls choices from the database to populate our select fields.
    """
    developers = Developer.query.all()
    developer_names = {'0':'Choose Developer'}

    for developer in developers:
        developer_names[developer.user_id] = developer.name

    developer_choices = [(k, v) for k, v in developer_names.iteritems()]
    form.developer_id.choices = developer_choices


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/app_assets/<int:app_id>', methods=['GET', 'POST'])
def app_assets(app_id):
    application = Application.query.filter_by(id=app_id).first()
    developer = Developer.query.filter_by(user_id=application.developer_id).first()

    form = ApplicationAssetsForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            APP_DIR = os.path.abspath(os.path.join(__file__ ,"../.."))
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
    developer = Developer.query.filter_by(user_id=application.developer_id)
    assets = ApplicationAssets.query.filter_by(application_id=app_id).first()

    return render_template('app_info.html', application=application, developer=developer, assets=assets)


@main.route('/application', methods=['GET', 'POST'])
def application():
    form = ApplicationsForm()
    populate_categories(form)
    populate_developers(form)

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
            APP_DIR = os.path.abspath(os.path.join(__file__ ,"../.."))
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

    if form.validate_on_submit():
        category = Category(name=form.name.data,
                    description=form.description.data)
        db.session.add(category)
        db.session.commit()

        flash('Category added successfully', 'success')
        return redirect(request.args.get('next') or url_for('main.category'))

    return render_template('category.html', form=form)
