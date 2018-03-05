from forms import LoginForm, RegisterForm, ListNewItemForm, SearchForm, ItemDescriptionForm, ItemRatingForm
from flask import Flask, request, session, redirect, url_for, render_template, flash
from data_access.user import User
from data_access.item import Item
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
            return redirect(url_for('login'))

    logging.debug("OUT register method")
    return render_template('register.html',
                           ui_data={},
                           form=form,
                           error=error)


@app.route('/list_new_item', methods=['GET', 'POST'])
def list_new_item():
    form = ListNewItemForm()
    error = None
    if form.validate_on_submit():

        msg = "now_sale_price='{}' type={}".format(request.form['now_sale_price'],type(request.form['now_sale_price']))
        logging.debug("PASSED form.validate_on_submit ["+ msg+"]")
        # todo need to run the business rules validations here before the INSERT
        returnable = False
        logging.debug("returns_accepted=[{}]".format(str(request.form)))
        if 'returns_accepted' in request.form:
            returnable = True

        now_sale_price = "NULL"
        if request.form['now_sale_price'] != "":
            now_sale_price = request.form['now_sale_price']

        item = Item(0,
                    request.form['item_name'],
                    request.form['description'],
                    request.form['category'],
                    request.form['condition'],
                    returnable,
                    #todo clean this strip replace up
                    request.form['start_bid'].strip('$').replace(',', ''),
                    request.form['min_sale_price'].strip('$').replace(',', ''),
                    request.form['auction_days'],
                    #todo start time is populated from the db
                    #passing here but likely not needed
                    datetime.now(),
                    session['user']['user_name'],
                    now_sale_price.strip('$').replace(',', '')
                    )
        logging.debug("passed constructor")
        item_id, error = item.persist()
        logging.debug("passed item.persist")
        if item_id is not None:
            logging.debug("passed if item_id is not None")
            flash("Your item {} is now in an auction".format(request.form['item_name']))
            return redirect(url_for('index'))
        logging.debug("exiting validation loop")


    return render_template('list_new_item.html',
                           ui_data={},
                           form=form,
                           error=error)


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    error = None
    logging.debug("search.....")
    if form.validate_on_submit():
        logging.debug("form.validate_on_submit()")
        # todo this needs clean up and DB on unique username
        return redirect(url_for('search_results'))

    logging.debug("form.errors={}".format(form.errors))

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
