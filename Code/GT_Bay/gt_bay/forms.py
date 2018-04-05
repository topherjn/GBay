import flask
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, DecimalField, SubmitField, BooleanField, HiddenField, PasswordField
from wtforms.validators import DataRequired, Regexp, Optional
from data_access.category import Category
from decimal import Decimal
import re
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class LoginForm(FlaskForm):
    user_name = StringField('user_name', validators=[DataRequired("Username is required.")])
    password = PasswordField('password', validators=[DataRequired("Password is required.")])
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired("First Name is required.")])
    last_name = StringField('last_name', validators=[DataRequired("Last Name is required.")])
    user_name = StringField('user_name', validators=[DataRequired("User Name is required.")])
    password = PasswordField('password', validators=[DataRequired("Password is required.")])
    confirm = PasswordField('confirm', validators=[DataRequired("Confirm is required.")])
    submit = SubmitField('Register')

    def validate(self):
        logging.debug("RegisterForm: In validate method")
        if not FlaskForm.validate(self):
            return False
        result = True
        if self.password.data != self.confirm.data:
            logging.debug("passwords not equal")
            self.confirm.errors.append('Password and confirm password are not equal.')
            result = False
        return result


class ListNewItemForm(FlaskForm):
    item_name = StringField('item_name', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    category_choices, error = Category.get_categories()
    # category_choices = [(1, 'Art'), (2, 'Books'), (3, 'Electronics'), (4, 'Home & Garden'), (5, 'Sporting Goods'), (6, 'Toys'), (7, 'Other')]
    category = SelectField('category', coerce=int, choices=category_choices)
    condition_choices = [(5, 'New'), (4, 'Very Good'), (3, 'Good'), (2, 'Fair'), (1, 'Poor')]
    condition = SelectField('condition', coerce=int, choices=condition_choices)
    start_bid = StringField('start_bid', validators=[DataRequired("Start bid price is required.")])
    min_sale_price = StringField('min_sale_price', validators=[DataRequired("Minimum sale price is required.")])
    auction_days_choices = [(1, '1 Day'), (3, '3 Days'), (5, '5 Days'), (7, '7 Days')]
    auction_days = SelectField('auction_days', coerce=int, choices=auction_days_choices)
    now_sale_price = StringField('now_sale_price')
    returns_accepted = BooleanField('returns_accepted', validators=[Optional()])
    submit = SubmitField('List New Item')


    def validate(self):
        logging.debug("ListNewItemForm: In validate method")
        if not FlaskForm.validate(self):
            return False
        result = True
        #todo add additional validation
        start_bid = self.str_to_currency(self.start_bid)
        min_sale_price = self.str_to_currency(self.min_sale_price)
        now_sale_price = self.str_to_currency(self.now_sale_price, optional=True)

        #todo / comment by Joy: append to each field's errors to give more specific error messages?
        if start_bid is None or min_sale_price is None:
            logging.debug("start_bid or min_sale_price is None")
            return False

        logging.debug("now_sale_price {}".format(now_sale_price))
        if now_sale_price is not None:
            if now_sale_price < min_sale_price:
                self.now_sale_price.errors.append('Buy now cannot be less than minimum sale')
                result = False
            if now_sale_price < start_bid:
                self.now_sale_price.errors.append('Buy now cannot be less than start bid')
                result = False
        logging.debug("checking start_bid > min_sale_price")
        if start_bid > min_sale_price:
            logging.debug("start_bid > min_sale_price")
            self.start_bid.errors.append('Starting bid cannot be greater than minimum sale')
            result = False

        return result


    #todo / comment by Joy: maybe allow more flexible input formats to have better user experience?
    def str_to_currency(self, field, optional=False):
        error = "Cannot convert input to US currency."
        amount = None
        logging.debug("field.data='{}'".format(field.data))
        if optional and field.data == "":
            logging.debug("jumping out cause it is optional")
            return amount

        str_amount = field.data.strip('$').replace(',', '')
        has_decimal_place = str_amount.count('.')
        if has_decimal_place == 1:
            decimal_place_index = str_amount.find('.')
            logging.debug("decimal_place_index={} after_dec={} len={}".
                          format(decimal_place_index,
                                 str_amount[decimal_place_index:],
                                 len(str_amount[decimal_place_index:])))
            should_be_three = len(str_amount[decimal_place_index:])
            if should_be_three == 3:
                try:
                    amount = float(str_amount)
                    field.data = "{0:.2f}".format(amount)
                except ValueError:
                    field.errors.append(error)
            else:
                logging.debug("yes we have an error")
                field.errors.append(error)
        else:
            field.errors.append(error+" please be sure to include dollars and cents 100.00")

        return amount


class SearchForm(FlaskForm):
    """Defines the fields of the Search Form and performs validation on said fields.

    """

    keyword = StringField('keyword', validators=[Optional()])
    category_choices, error = Category.get_categories()
    category_choices.insert(0,(0,' '))  # add blank, default "category"
    category = SelectField('category', coerce=int, choices=category_choices)
    minimum_price = StringField('minimum_price', validators=[Optional()])
    maximum_price = StringField('maximum_price', validators=[Optional()])
    condition_choices = [(0,' '),(5, 'New'), (4, 'Very Good'), (3, 'Good'), (2, 'Fair'), (1, 'Poor')]
    condition = SelectField('condition', coerce=int, choices=condition_choices)
    submit = SubmitField('Search')

    def validate(self):
        """Performs validation on Search Form fields.

        :return: False is returned if an error is encountered. If all is well, True is returned.
        """

        logging.debug("\n\nSearchForm: In validate method")
        usd = True
        result = True
        if not FlaskForm.validate(self):  # only using this for the "DataRequired" validator for the keyword field
            result = False

        # minimum/maximum price validation: START
        errorMsg = 'Cannot convert input to US currency. Please be sure to include dollars and cents (e.g., 100.00)'
        is_dollar_amt = "^[+-]?[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2}$"
        rePatternObj = re.compile(is_dollar_amt)

        logging.debug("\n\tforms.validate: self.minimum_price.errors = {}".format(self.minimum_price.errors))
        logging.debug("\t\tforms.validate: self.minimum_price.data = {}".format(self.minimum_price.data))
        if (self.minimum_price.data is not None) and (self.minimum_price.data != '') \
                and (rePatternObj.match(str(self.minimum_price.data)) is None):
            logging.debug("minimum_price not USD")
            self.minimum_price.errors.append(errorMsg)
            usd = False
            result = False

        logging.debug("\n\tforms.validate: self.maximum_price.errors = {}".format(self.maximum_price.errors))
        logging.debug("\t\tforms.validate: self.maximum_price.data = {}".format(self.maximum_price.data))
        if (self.maximum_price.data is not None) and (self.maximum_price.data != '') and \
                (rePatternObj.match(str(self.maximum_price.data)) is None):
            logging.debug("\tforms.validate: maximum_price not USD")
            self.maximum_price.errors.append(errorMsg)
            usd = False
            result = False

        if (self.minimum_price.data is not None) and (self.maximum_price.data is not None) and \
                (self.minimum_price.data != '') and (self.maximum_price.data != '') and usd:
            if self.minimum_price.data > self.maximum_price.data:  # minimum price must be less than maximum price
                logging.debug("\tforms.validate: maximum price is not greater than the minimum_price")
                self.maximum_price.errors.append('The maximum price must be greater than the minimum price.')
                result = False
        # minimum/maximum price validation: END

        return result


class ItemBiddingForm(FlaskForm):
    item_id = HiddenField('item_id')
    your_bid = DecimalField('your_bid', validators=[DataRequired()])
    min_bid = HiddenField('min_bid')
    getnow_price = HiddenField('getnow_price')
    submit = SubmitField('Bid On This Item')

    def validate(self):
        logging.debug("\n\nItemBiddingForm: In validate method")
        result = True

        # your_bid field is required and is a number
        if not FlaskForm.validate(self):  
            result = False
            self.your_bid.errors.append("Only number accepted (e.g. 100.00)")
            return result

        # your_bid has at most 2 decimal places
        bid_amount = self.your_bid.data
        if str(bid_amount).count('.') == 1 and len(str(bid_amount)[str(bid_amount).find('.'):]) > 3:
            result = False
            self.your_bid.errors.append("At most 2 decimal places accepted (e.g. 100.00)")

	# check the value of your_bid
        logging.debug("\n\tItemBiddingForm.validate: {} {} {} {}".
                      format(self.item_id, self.your_bid, self.min_bid, self.getnow_price))
        if bid_amount < Decimal(self.min_bid.data):
            result = False
            self.your_bid.errors.append("Your bid must be at least the minimum bid ${}".format(self.min_bid.data))
        if self.getnow_price.data != '' and bid_amount >= Decimal(self.getnow_price.data):
            result = False
            self.your_bid.errors.append("Your bid exceeds the get it now price, please use the Get It Now purchase option")

        return result


class ItemRatingForm(FlaskForm):
    item_id = StringField('itemid')
    username = HiddenField('username')
    numstars = HiddenField('numstars')
    comments = TextAreaField('comments')
    submit = SubmitField('AAdd Rating')