from app.models import Application, ApplicationAssets, Category
from flask import current_app


def add_category():
    category = Category.query().all()


def add_application():
    application = Application.query().all()
