import functools
from functools import wraps

from flask import g, flash, redirect, url_for, request
def requires_login(f):
   def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "some_admin_name" in session:
            return f(*args, **kwargs)
        else:
            flash("\"You shall not pass!\" - Gandalf")
            return redirect(url_for("login"))
    return wrap