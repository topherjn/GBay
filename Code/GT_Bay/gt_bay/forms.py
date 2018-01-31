from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, DecimalField, BooleanField, HiddenField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    user_name = StringField('user_name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    user_name = StringField('user_name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm = PasswordField('confirm', validators=[DataRequired()])

class ListNewItemForm(FlaskForm):
    item_name = StringField('item_name', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    category_choices = [('art', 'Art'), ('books', 'Books'), ('electronics', 'Electronics'), ('home', 'Home & Garden'), ('sports', 'Sporting Goods'), ('toys', 'Toys'), ('other', 'Other')]
    category = SelectField('category', choices=category_choices, validators=[DataRequired()])
    condition_choices = [('50', 'New'), ('40', 'Very Good'), ('30', 'Good'), ('20', 'Fair'), ('10', 'Poor')]
    condition = SelectField('condition', choices=condition_choices, validators=[DataRequired()])
    start_bid = DecimalField('start_bid', validators=[DataRequired()])
    min_sale_price = DecimalField('min_sale_price', validators=[DataRequired()])
    auction_days_choices = [('1', '1 Day'), ('3', '3 Days'), ('5', '5 Days'), ('7', '7 Days')]
    auction_days = SelectField('auction_days', choices=auction_days_choices, validators=[DataRequired()])
    now_sale_price = DecimalField('now_sale_price', validators=[DataRequired()])
    returns_accepted = BooleanField('returns_accepted', validators=[DataRequired()])

class SearchForm(FlaskForm):
    keyword = StringField('keyword', validators=[DataRequired()])
    category_choices = [('art', 'Art'), ('books', 'Books'), ('electronics', 'Electronics'), ('home', 'Home & Garden'), ('sports', 'Sporting Goods'), ('toys', 'Toys'), ('other', 'Other')]
    category = SelectField('category', choices=category_choices, validators=[DataRequired()])
    minimum_price = DecimalField('minimum_price', validators=[DataRequired()])
    maximum_price = DecimalField('maximum_price', validators=[DataRequired()])
    condition_choices = [('50', 'New'), ('40', 'Very Good'), ('30', 'Good'), ('20', 'Fair'), ('10', 'Poor')]
    condition = SelectField('condition', choices=condition_choices, validators=[DataRequired()])

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

