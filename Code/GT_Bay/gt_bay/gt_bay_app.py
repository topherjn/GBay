from forms import LoginForm, RegisterForm, ListNewItemForm, SearchForm, ItemBiddingForm, ItemRatingForm, \
    itemEditDescForm
from flask import Flask, request, session, redirect, url_for, render_template, flash
from data_access.user import User
from data_access.item import Item
from data_access.report import Report
from data_access.rating import Rating
from datetime import datetime
import logging


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , flaskr.py
#app.debug = True

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

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
            flash('You were logged in.')
            return redirect(url_for('index'))

    return render_template('login.html',
                           ui_data={},
                           form=form,
                           error=error)


@app.route('/logout')
def logout():
    """Pops session variables and re-routes to index.

    :return: None
    """

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
            # session['user'] = user.to_json()
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
    logging.debug("\n\n\tgt_bay_app.search: START")
    form = SearchForm()
    error = None

    if form.validate_on_submit():
        logging.debug("\tgt_bay_app.search: form.validate_on_submit()")

        minimum_price = "NULL"
        minPriceFormVal = request.form['minimum_price']
        if minPriceFormVal != "":
            minimum_price = float(minPriceFormVal)

        maximum_price = "NULL"
        maxPriceFormVal = request.form['maximum_price']
        if maxPriceFormVal != "":
            maximum_price = float(maxPriceFormVal)

        item = Item()
        search_results, error = item.search(
            request.form['keyword'],
            request.form['category'],
            minimum_price,
            maximum_price,
            request.form['condition']
        )

        if search_results is not None:
            return render_template('search_results.html', search_results=search_results, error=error)

    logging.debug("\t\tgt_bay_app.search.valid: form.errors={}".format(form.errors))

    return render_template('search.html', ui_data={}, form=form, error=error)


@app.route('/get_item', methods=['GET', 'POST'])
def get_item():
    item_id = request.args.get('id')
    form = ItemBiddingForm()
    placeBid_result = None
    placeBid_error = None

    if form.validate_on_submit():
        logging.debug("\tgt_bay_app.get_item: form.validate_on_submit()")

        placeBid_result, placeBid_error = Item.place_bid(
           request.form['item_id'],
           request.form['your_bid'],
           session['user']['user_name']
        )

        if placeBid_error is not None:
           flash("Database access failure: {}".format(placeBid_error))
        elif placeBid_result < 1:
           flash("Bid not placed: be outbid or auction ends")
        else:
           flash("Bid successfully placed at ${0:.2f}".format(float(request.form['your_bid'])))

        return redirect(url_for('get_item', id=item_id))

    logging.debug("\t\tgt_bay_app.get_item.valid: form.errors={}".format(form.errors))
       
    form.item_id.data = item_id

    item, error = Item.get_item(item_id)
    if item is None:
        logging.debug("/get_item: item is None")
        flash("Failed to get Item ID {item_id}: {error}".format(item_id=item_id, error=error))
        return redirect(url_for('index'))

    form.item_name.data = item[0]
    form.desc.data = item[1]

    form.getnow_price.data = item[5]

    bids, getBids_error = Item.get_bids(item_id)

    min_bid, mb_error = Item.get_min_bid(item_id)
    form.min_bid.data = min_bid[0]

    return render_template('item_description.html', ui_data={}, form=form,
                           item=item, bids=bids, getBids_error=getBids_error, mb_error=mb_error)


@app.route('/get_now')
def get_now():
    item_id = request.args.get('id')
    result = None
    error = None

    result, error = Item.get_now(
      item_id,
      session['user']['user_name']
    )

    if error is not None:
      flash("Database access failure: {}".format(error))
    elif result < 1:
      flash("Get It Now failed")
    else:
      flash("Item successfully purchased by Get It Now")

    return redirect(url_for('get_item', id=item_id))


@app.route('/item_rating', methods=['GET', 'POST'])
def item_rating():
    item_id = request.args.get('id')
    form = ItemRatingForm()
    rating = Rating()
    ret_val, error = rating.get_rating(item_id)

    if ret_val is not None:
        form.item_id.data = item_id
        form.average_rating = ret_val

        
    return render_template('item_rating.html',ui_data={},form=form,
                           error=error)

@app.route('/item_edit_desc', methods=['GET', 'POST'])
def item_edit_desc():
    item_id = request.args.get('id')
    item_name = request.args.get('name')
    desc = request.args.get('desc')
    form = itemEditDescForm()
    form.item_id.data = item_id
    form.item_name.data = item_name
    form.description.data = desc

    error = None
    logger.debug("\tgt_bay_app.item_edit_desc: form.description.data = {}".format(form.description.data))
    if form.validate_on_submit():
        logging.debug("\tgt_bay_app.item_edit_desc: form.validate_on_submit()")
        desc = request.form['description']
        logging.debug("\t\tgt_bay_app.item_edit_desc: form.validate_on_submit() - desc = {}".format(desc))
        retval, error = Item.updateDesc(item_id=item_id, desc=desc)
        logging.debug("\t\tgt_bay_app.item_edit_desc: form.validate_on_submit() - error = {}".format(error))

        if error is None:
            return redirect(url_for('get_item', id=item_id))
    else:
        logging.debug("\t\tgt_bay_app.py - item_edit_desc.form.validate_on_submit(): ELSE")

    return render_template('item_edit_desc.html', ui_data={}, form=form, error=error)
    #return redirect(url_for('item_edit_desc.html', id=item_id, name=item_name, desc=desc))

@app.route('/search_results')
def search_results():
    return render_template('search_results.html', ui_data={})

@app.route('/auction_results')
def auction_results():
    return render_template('auction_results.html', ui_data={})

@app.route('/category_report')
def category_report():
    report = Report()
    cat_report, error = report.category_report()
    return render_template('category_report.html', cat_report=cat_report, error=error)

@app.route('/user_report')
def user_report():
    return render_template('user_report.html', ui_data={})

# Load default config and override config from an environment variable
app.debug = True
app.config.update(dict(
    SECRET_KEY='development key',
    WTF_CSRF_ENABLED=True,
))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
    # app.run(host='0.0.0.0')
