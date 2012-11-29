from EasyDraft import app, database, login_manager
from flask import g, render_template, redirect, request, url_for, flash
from database.database import Database
from flask.ext.login import LoginManager, current_user, login_required, login_user, logout_user
from forms import LoginForm, RegistrationForm


@login_manager.user_loader
def load_user(user_id):
    return database.get_user(user_id)

@app.route('/')
def index():
    rows = database.get_user("a")
    return render_template('index.html')

@app.route("/accounts/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = False
    if request.method == 'POST' and form.validate():
        user = database.get_user(form.email.data, form.password.data)
        if user is not None:
            login_user(user)
            return redirect(request.args.get("next") or url_for("index"))
        else:
            error=True
    return render_template("accounts/login.html", form=form, error=error)

@app.route("/accounts/logout/")
@login_required
def logout():
    logout_user()
    return redirect(request.args.get("next") or url_for("index"))

@app.route("/accounts/register/", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        database.insert_user(form.email.data, form.password.data)
        flash("Successfully Registered!")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("accounts/register.html", form=form)

