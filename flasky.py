from flask import Flask
from flask import request
from flask import render_template
from flask import session, redirect,url_for, flash
from flask.cli import FlaskGroup
from datetime import datetime
from werkzeug.middleware.proxy_fix import ProxyFix
import sys
import os.path


from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from flaskext.markdown import Markdown

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)


filename = 'secret_key'
app.config['SECRET_KEY'] = open(filename, 'rb').read()

cli=FlaskGroup(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
Markdown(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[InputRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'))

@app.route('/user/<name>')
def user(name):

    user_agent = request.headers.get('User-Agent')
    return render_template('user.html', name=name, user_agent=user_agent)

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/blog')
def blog():
    mkd_text="## Welcome to the Blog"
    with open('iceland.md','r') as f:
        mkd_text=f.read()
    return render_template('blog.html',mkd_text=mkd_text)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
        return render_template('500.html'), 500


