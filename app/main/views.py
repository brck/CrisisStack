from flask import render_template, request, redirect, url_for, flash
from werkzeug import secure_filename
from flask import current_app
import os
from . import main
from ..models import Category
from .. import db
from .forms import ApplicationsForm, CategoryForm

ALLOWED_EXTENSIONS = set(['sh'])


def populate_categories(form):
    """
    Pulls choices from the database to populate our select fields.
    """
    categories = Category.query.all()
    category_names = {'0':'Choose Category'}

    for category in categories:
        category_names[category.id] = category.name
    category_choices = [(k, v) for k, v in category_names.iteritems()]
    #now that we've built our choices, we need to set them.
    form.category_id.choices = category_choices


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/app_info')
def app_info():
    return render_template('app_info.html')


@main.route('/application', methods=['GET', 'POST'])
def application():
    form = ApplicationsForm()
    populate_categories(form)

    if form.validate_on_submit():
        print request.form
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
            #file.save(os.path.join(INSTALLS_DIR, filename))

            size = os.stat(FILE_PATH).st_size
            print 'file size', size

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
