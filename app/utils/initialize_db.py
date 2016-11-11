import os
import uuid
import json
from shutil import copyfile
from flask import current_app
from app import db
from sqlalchemy.exc import IntegrityError
from app.models import Application, ApplicationAssets, Category, User, Developer


class InitDb():
    def create_applications_folder(self, app_uuid):
        APPLICATIONS_DIR = current_app.config['APPLICATIONS_DIR']

        APP_DIR = os.path.join(APPLICATIONS_DIR, str(app_uuid))
        if not os.path.exists(APP_DIR):
            os.makedirs(APP_DIR)

        ASSETS_DIR = os.path.join(APP_DIR, 'assets')
        if not os.path.exists(ASSETS_DIR):
            os.makedirs(ASSETS_DIR)

        return {'APP_DIR': APP_DIR, 'ASSETS_DIR': ASSETS_DIR}

    def add_categories(self):
        if Category.query.count() < 1:
            category = Category(name="Default Apps", description="Preloaded first responder crisis applications")
            db.session.add(category)
            db.session.commit()

    def add_developers(self):
        developers = [
            {"email": "ushahidi@cs.com", "name": "Ushahidi", "website": "http://ushahidi.com"},
            {"email": "enketo@cs.com", "name": "Enketo", "website": "http://enketo.com"},
            {"email": "etherpad@cs.com", "name": "Etherpad", "website": "http://etherpad.com"},
            {"email": "sahana@cs.com", "name": "Sahana", "website": "http://sahana.com"}
        ]
        if Developer.query.count() < 1:
            try:
                for dev in developers:
                    user = User(email=dev['email'],
                                username=dev['name'],
                                password=dev['name'])
                    db.session.add(user)
                    db.session.flush()

                    developer = Developer(
                        user_id=user.id,
                        name=dev['name'],
                        website=dev['website'])

                    db.session.add(developer)

                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()

    def add_applications(self):
        start_path = current_app.config['DEFAULT_APPS_DIR']
        folders = [folder for folder in os.listdir(start_path)]
        app_ext = ['sh', 'deb', 'npm']

        default_apps = []

        for folder in folders:
            folder_path = os.path.join(start_path, folder)
            if os.path.isdir(folder_path):
                files = [f for f in os.listdir(folder_path)]
            default_app = {}
            for f in files:
                file_ext = f.rsplit('.', 1)[1]
                if file_ext in app_ext:
                    default_app['app_name'] = f.rsplit('.', 1)[0]
                    default_app['file_name'] = f
                    default_app['folder_path'] = folder_path

                elif file_ext == 'json':
                    data_file_path = os.path.join(folder_path, f)
                    with open(data_file_path, 'r') as f:
                        data = json.load(f)

                    default_app['category_id'] = data[0]['category_id']
                    default_app['developer_id'] = data[0]['developer_id']
                    default_app['version'] = data[0]['version']
                    default_app['description'] = data[0]['description']
                    default_app['permission'] = data[0]['permission']
                    default_app['osVersion'] = data[0]['osVersion']
                    default_app['launchurl'] = data[0]['launchurl']
                else:
                    default_app[f.rsplit('.', 1)[0]] = f

            default_apps.append(default_app)
            app_uuid = str(uuid.uuid4())
            app_name = default_app['app_name']

            if not Application.query.filter_by(name=app_name).first():
                APP_FOLDERS = self.create_applications_folder(app_uuid)

                filename = default_app['file_name']
                SRC_PATH = os.path.join(default_app['folder_path'], filename)
                DEST_PATH = os.path.join(APP_FOLDERS.get('APP_DIR'), filename)

                copyfile(SRC_PATH, DEST_PATH)

                size = os.stat(DEST_PATH).st_size
                app_name = default_app['app_name']

                application = Application(
                    uuid=app_uuid,
                    category_id=default_app['category_id'],
                    developer_id=default_app['developer_id'],
                    name=app_name,
                    version=default_app['version'],
                    description=default_app['description'],
                    size=size,
                    permission=default_app['permission'],
                    osVersion=default_app['osVersion'],
                    launchurl=default_app['launchurl'],
                    application_status='Active')

                db.session.add(application)

                ASSETS_DIR = APP_FOLDERS.get('ASSETS_DIR')
                excluded_files = ['sh', 'json', 'deb', 'rpm']
                for f in files:
                    file_ext = f.rsplit('.', 1)[1]
                    SRC_PATH = os.path.join(folder_path, f)
                    DEST_PATH = os.path.join(APP_FOLDERS.get('ASSETS_DIR'), f)
                    if file_ext not in excluded_files:
                        copyfile(SRC_PATH, DEST_PATH)
                    pass

                assets = ApplicationAssets(
                    app_uuid=app_uuid,
                    icon=default_app.get('icon', 'app_icon.png'),
                    screenShotOne=default_app.get('screenshot1', 'browser.png'),
                    screenShotTwo=default_app.get('screenshot2', 'browser.png'),
                    screenShotThree=default_app.get('screenshot3', 'browser.png'),
                    screenShotFour=default_app.get('screenshot4', 'browser.png'),
                    video=default_app.get('video', 'None'))

                db.session.add(assets)

        db.session.commit()
