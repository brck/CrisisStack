from flask_wtf import Form
from wtforms import SubmitField, TextAreaField, validators, PasswordField, SelectField, StringField, BooleanField, ValidationError, FileField
from ..models import Application


class ApplicationsForm(Form):
    """Applications update form"""
    version = StringField("Version", [
        validators.DataRequired("Enter application version.")],
        render_kw={"placeholder": "Version"})
    description = StringField("Description", [
        validators.DataRequired("Enter application description.")],
        render_kw={"placeholder": "Description"})
    file = FileField("Size", [
        validators.DataRequired("Application size can not be blank")],
        render_kw={"placeholder": "Size"})
    app_permissions = [
        ('0', 'Choose App OS Permissions'),
        ('OS-Admin', 'OS-Admin'),
        ('None', 'None')
    ]
    permission = SelectField(label="Permissions", choices = app_permissions, default = ['0'])
    os_vesions = [
        ('0', 'Choose OS'),
        ('Raspbian', 'Raspbian'),
        ('Ubuntu MATE', 'Ubuntu MATE'),
        ('FreeBSD', 'FreeBSD')
    ]
    osVersion = SelectField(label="OS Version", choices = os_vesions, default = ['0'])
    category_id = SelectField(label="Category", coerce=int)
    developer_id = SelectField(label="Developer", coerce=int)
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


class ApplicationAssetsForm(Form):
    """Applications update form"""
    icon = FileField("Icon", [
        validators.DataRequired("Application Icon can not be blank")],
        render_kw={"placeholder": "Icon"})
    screenshot1 = FileField("Screen Shot One", [
        validators.DataRequired("Application Screen Shot can not be blank")],
        render_kw={"placeholder": "Screen Shot One"})
    screenshot2 = FileField("Screen Shot One", [
        validators.DataRequired("Application Screen Shot can not be blank")],
        render_kw={"placeholder": "Screen Shot One"})
    screenshot3 = FileField("Screen Shot One", [
        validators.DataRequired("Application Screen Shot can not be blank")],
        render_kw={"placeholder": "Screen Shot One"})
    screenshot4 = FileField("Screen Shot One", [
        validators.DataRequired("Application Screen Shot can not be blank")],
        render_kw={"placeholder": "Size"})
    video = FileField("Screen Shot One", [
        validators.DataRequired("Application Video can not be blank")],
        render_kw={"placeholder": "Size"})

    submit = SubmitField("Login")

    def __init__(self, *args, **kwargs):
        super(ApplicationAssetsForm, self).__init__(*args, **kwargs)
