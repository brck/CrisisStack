from flask_wtf import Form
from wtforms import SubmitField, TextAreaField, validators, PasswordField, SelectField, StringField, BooleanField, ValidationError, FileField
from ..models import Application


class ApplicationsForm(Form):
    """Applications update form"""
    name = StringField("Name", [
        validators.DataRequired("Please enter the application name.")],
        render_kw={"placeholder": "Name"})
    version = StringField("Version", [
        validators.DataRequired("Enter application version.")],
        render_kw={"placeholder": "Version"})
    description = StringField("Description", [
        validators.DataRequired("Enter application description.")],
        render_kw={"placeholder": "Description"})
    file = FileField("Size", [
        validators.DataRequired("Application size can not be blank")],
        render_kw={"placeholder": "Size"})
    permission = StringField("Permission", [
        validators.DataRequired("Enter permissions needed by the application.")],
        render_kw={"placeholder": "Permission"})

    my_choices = [('0', 'Choose OS'), ('1', 'Raspbian'), ('2', 'Ubuntu MATE'), ('3', 'FreeBSD')]
    osVersion = SelectField(label="Category", choices = my_choices, default = ['0'])
    # osVersion = StringField("OS Version", [
    #     validators.DataRequired("Choose OS Version.")],
    #     render_kw={"placeholder": "OS Version"})
    category_id = SelectField(label="Category", coerce=int)
    # category_id = StringField("Category", [
    #     validators.DataRequired("Choose application category.")],
    #     render_kw={"placeholder": "Category"})
    launchurl = StringField("Launch URL", [
        validators.DataRequired("Please enter the launch url."),
        validators.url("Please enter a valid url.")],
        render_kw={"placeholder": "Launch URL"})

    submit = SubmitField("Login")

    def __init__(self, *args, **kwargs):
        super(ApplicationsForm, self).__init__(*args, **kwargs)


class CategoryForm(Form):
    """Applications update form"""
    name = StringField("Name", [
        validators.DataRequired("Please enter the Category name.")],
        render_kw={"placeholder": "Name"})

    description = TextAreaField("Description", [
        validators.DataRequired("Please enter the Description for this Category.")],
        render_kw={"placeholder": "Description"})

    submit = SubmitField("Login")

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
