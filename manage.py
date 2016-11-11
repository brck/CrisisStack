#!/usr/bin/env python
import os
cov = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    cov = coverage.coverage(branch=True, include='app/*')
    cov.start()

from app import create_app, db
from app.models import (User, Developer, Category, Application, ApplicationAssets,
                        ApplicationUpdates)
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Category=Category, Developer=Developer,
                Application=Application, ApplicationUpdates=ApplicationUpdates,
                ApplicationAssets=ApplicationAssets)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if cov:
        cov.stop()
        cov.save()
        print('Coverage Summary:')
        cov.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'coverage')
        cov.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        cov.erase()


@manager.command
def init_app():
    """Run database initialization."""
    from flask_migrate import init, migrate, upgrade

    # initialize migtrations
    migrations_dir = os.path.join(app.config['ROOT_DIR'], 'migrations')
    if not os.path.exists(migrations_dir):
        init()

    # perform database migrations
    migrate()

    # migrate database to latest revision
    upgrade()

    print "Migrations completed ........................................."

    # initialize database with default records
    from app.utils.initialize_db import InitDb
    init_db = InitDb()

    init_db.add_categories()
    init_db.add_developers()
    init_db.add_applications()

    print "Database records added ......................................."


if __name__ == '__main__':
    manager.run()
