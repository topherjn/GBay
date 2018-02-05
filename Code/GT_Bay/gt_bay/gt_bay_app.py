from forms import LoginForm, RegisterForm, ListNewItemForm, SearchForm, ItemDescriptionForm, ItemRatingForm
from flask import Flask, request, session, redirect, url_for, render_template, flash
from data_access.user import User
from datetime import datetime
from dateutil import tz
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , flaskr.py


# Retieve data from 'static' directory. Used most typically for rendering images.
@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.route('/')
@app.route('/index')
def index():
    ui_data = {}
    logging.debug("ui_data [{}]".format(ui_data))
    return render_template('index.html', ui_data=ui_data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        logging.debug("user_name={}, password={}".format(request.form['user_name'], request.form['password']))
        user, error = User.login(request.form['user_name'], request.form['password'])
        logging.debug("user={}, error={}".format(user, error))
        if user is not None:
            session['user'] = user.to_json()
            return redirect(url_for('index'))

    return render_template('login.html',
                           ui_data={},
                           form=form,
                           error=error)


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You were logged out')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    error = None
    logging.debug("IN register method")
    if form.validate_on_submit():
        logging.debug("PASSED form.validate_on_submit")
        user, error = User.register_user(request.form['user_name'], request.form['password'],
                                         request.form['first_name'], request.form['last_name'])
        if user is not None:
            session['user'] = user.to_json()
            return redirect(url_for('index'))

    logging.debug("OUT register method")
    return render_template('register.html',
                           ui_data={},
                           form=form,
                           error=error)


@app.route('/list_new_item', methods=['GET', 'POST'])
def list_new_item():
    form = ListNewItemForm()
    error = None
    if request.method == 'POST':
        # todo this needs clean up and DB on unique username
        if len(request.form['item_name']) == 0:
            error = 'Item Name is required'
        else:
            # todo add user to db
            return redirect(url_for('index'))

    return render_template('list_new_item.html',
                           ui_data={},
                           form=form,
                           error=error)


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    error = None
    if request.method == 'POST':
        # todo this needs clean up and DB on unique username
        if len(request.form['keyword']) == 0:
            error = 'Keyword is required'
        else:
            # todo add user to db
            return redirect(url_for('search_results'))

    return render_template('search.html',
                           ui_data={},
                           form=form,
                           error=error)


@app.route('/item_description', methods=['GET', 'POST'])
def item_description():
    form = ItemDescriptionForm()
    error = None
    return render_template('item_description.html', ui_data={},form=form,
                           error=error)

@app.route('/item_rating', methods=['GET', 'POST'])
def item_rating():
    form = ItemRatingForm()
    error = None
    return render_template('item_rating.html', ui_data={},form=form,
                           error=error)


@app.route('/search_results')
def search_results():
    return render_template('search_results.html', ui_data={})

@app.route('/auction_results')
def auction_results():
    return render_template('auction_results.html', ui_data={})

@app.route('/category_report')
def category_report():
    return render_template('category_report.html', ui_data={})

@app.route('/user_report')
def user_report():
    return render_template('user_report.html', ui_data={})

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='development key',
    WTF_CSRF_ENABLED=True,
))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
    # app.run(host='0.0.0.0')
