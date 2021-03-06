from flask import Flask, g, render_template, flash, redirect, url_for, abort
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user

import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key="asdfadsf"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
	try:
		return models.User.get(models.User.id == userid)
	except models.DoesNotExist:
		return None

@app.route('/')
def index():
  tacos = models.Taco.select()
  return render_template("index.html", tacos=tacos)

@app.route('/login', methods=('GET', 'POST'))
def login():
  form = forms.LoginForm()
  
  if form.validate_on_submit():
    try:
      user = models.User.select().where(models.User.email == form.email.data).get()
    except models.DoesNotExist:
      flash("Your email or password does not match!")
    else:
      if check_password_hash(user.password, form.password.data):
        login_user(user)
        flash("You've been logged in")
        return redirect(url_for('index'))
      else:
        flash("Your email or password does not match!")
  
  return render_template('login.html', form = form)

@app.route('/logout')
@login_required
def logout():
  logout_user()
  flash("You've been logged out!")
  return redirect(url_for('index'))

@app.route('/register', methods=('GET', 'POST'))
def register():
  form = forms.SignUpForm()
  
  if form.validate_on_submit():
    flash("You have registered")
    try:
      models.User.create_user(email=form.email.data, password=form.password.data)
    except ValueError as e:
      print(e)
    return redirect(url_for('index'))
  
  return render_template("register.html", form=form)


@app.route('/taco', methods=('GET', 'POST'))
@login_required
def newTaco():
  form = forms.TacoForm()
  
  if form.validate_on_submit():
    models.Taco.create(protein=form.protein.data.strip(), shell=form.shell.data.strip(), cheese=form.cheese.data, extras=form.extras.data.strip(), user=g.user._get_current_object())
    flash("Taco added")
    return redirect(url_for('index'))
  
  return render_template("taco.html", form=form)

@app.before_request
def before_request():
  g.db = models.DATABASE
  g.db.connect()
  g.user = current_user
  
@app.after_request
def after_request(response):
  g.db.close()
  return response

if __name__ == '__main__':
  models.initialize()
  #app.run(debug=DEBUG, host=HOST, port=PORT)
