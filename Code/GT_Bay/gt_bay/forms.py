from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, DecimalField, SubmitField, BooleanField, HiddenField, PasswordField
from wtforms.validators import DataRequired, Regexp, Optional
from data_access.category import Category
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
        logging.debug("In validate method")
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
        logging.debug("In validate method")
        if not FlaskForm.validate(self):
            return False
        result = True
        #todo add additional validation
        start_bid = self.str_to_currency(self.start_bid)
        min_sale_price = self.str_to_currency(self.min_sale_price)
        now_sale_price = self.str_to_currency(self.now_sale_price, optional=True)

        if start_bid is None or min_sale_price is None:
            logging.debug("start_bid or min_sale_price is None")
            return False

        logging.debug("now_sale_price {}".format(now_sale_price))
        if now_sale_price is not None:
            if now_sale_price <  min_sale_price:
                self.now_sale_price.errors.append('Buy now cannot be less than minimum sale')
                result = False
            if now_sale_price <  start_bid:
                self.now_sale_price.errors.append('Buy now cannot be less than start bid')
                result = False
        logging.debug("checking start_bid > min_sale_price")
        if start_bid > min_sale_price:
            logging.debug("start_bid > min_sale_price")
            self.start_bid.errors.append('Starting bid cannot be greater than minimum sale')
            result = False

        return result

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
                logging.debug("yes we have and error")
                field.errors.append(error)
        else:
            field.errors.append(error+" please be sure to include dollars and cents 100.00")

        return amount

class SearchForm(FlaskForm):
    keyword = StringField('keyword', validators=[DataRequired("Keyword data is required")])
    category_choices, error = Category.get_categories()
    category_choices.insert(0,(0,' '))
    category = SelectField('category', choices=category_choices)
    is_dollar_amt="^[+-]?[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2}$"

    minimum_price = DecimalField('minimum_price',validators=[Optional()])
    maximum_price = DecimalField('maximum_price',validators=[Optional()])
    condition_choices = [(0,' '),(50, 'New'), (40, 'Very Good'), (30, 'Good'), (20, 'Fair'), (10, 'Poor')]
    condition = SelectField('condition', choices=condition_choices)
    submit = SubmitField('Search')


class ItemDescriptionForm(FlaskForm):
    item_id = StringField('item_id')
    item_name = StringField('item_name')
    description = TextAreaField('description')
    category = StringField('category')
    condition = StringField('condition')
    returns_accepted = BooleanField('returns_accepted')
    now_sale_price = DecimalField('now_sale_price')
    auction_end_dt = StringField('auction_end_dt')
    your_bid = DecimalField('your_bid', validators=[DataRequired()])
    min_bid = DecimalField('min_bid')

class ItemRatingForm(FlaskForm):
    item_id = StringField('item_id')
    item_name = StringField('item_name')
    average_rating = StringField('average_rating')
    comments = TextAreaField('comments')

