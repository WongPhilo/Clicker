import os
import re
from flask import Flask, render_template, session, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object(__name__)

app.config['SECRET_KEY'] = 'secret key' #change this!
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    clicks = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % self.username

class NameForm(FlaskForm):
    name = StringField('Input a username?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e=None):
	return render_template('404.html', title='404'), 404

@app.errorhandler(500)
def internal_server_error(e=None):
	return render_template('500.html', title='500'), 500

@app.route('/increment', methods=['POST'])
def increment():
    ret_json = request.get_json()

    user = ret_json['username']
    nclicks = int(ret_json['clicks'])

    dbuser = db.session.query(User).filter_by(username=user).first()
    dbuser.clicks = nclicks

    db.session.commit()
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    db.create_all()
    if (User.query.first() == None):
        null_user = User(username='null', clicks=0)
        db.session.add(null_user)
        db.session.commit()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data, clicks=0)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    
    sql = ("SELECT * FROM Users;")
    result = db.session.execute(text(sql))

    sname = session.get('name')
    if (sname == None):
         sname = 'null'
    sql = ("SELECT clicks FROM Users WHERE username = '" + sname + "';")
    nclicks = re.sub('\D', '', str(db.session.execute(text(sql)).mappings().all()))

    return render_template('index.html', form = form, name = sname, nclicks = nclicks, data = result)