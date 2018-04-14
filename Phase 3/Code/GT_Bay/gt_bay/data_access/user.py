import logging
from data_access.sql_statements import SQLStatements
from pymysql import IntegrityError

from data_access.base_data_access_object import BaseDAO

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class User(BaseDAO):
    def __init__(self, user_name, position=None, password=None, first_name=None, last_name=None):
        self._user_name = user_name
        self._password = password
        self._first_name = first_name
        self._last_name = last_name
        self._position = position

    @property
    def user_name(self):
        return self._user_name

    @property
    def password(self):
        return self._password

    @property
    def position(self):
        return self._position

    @property
    def is_admin(self):
        if self._position is not None:
            return True
        else:
            return False

    def to_json(self):
        dict = {'user_name': self._user_name, 'position': self._position}
        return dict


    @staticmethod
    def login(user_name, password):
        ret_val = None
        error = None
        logging.debug("login user_name={}, password={}".format(user_name, password))
        db = User.get_db()

        select_gt_bay_user = SQLStatements.select_gt_bay_user.format(
            db.escape_string(user_name), db.escape_string(password))

        try:
            cursor = db.cursor()
            cursor.execute(select_gt_bay_user)
            db_result = cursor.fetchone()
            if db_result is None:
                error = "Username and or password is incorrect."
            else:
                ret_val = User(db_result[0], db_result[1])

            logging.debug("data {}".format(db_result))
        except:
            error = "Unable to connect please try again later."

        return ret_val, error

    @staticmethod
    def register_user(user_name, password, first_name, last_name):
        ret_val = None
        error = None
        logging.debug("register_user user_name={}, password={}".format(user_name, password))

        db = User.get_db()
        insert_regular_user = SQLStatements.insert_regular_user.format(
            db.escape_string(user_name),
            db.escape_string(password),
            db.escape_string(first_name),
            db.escape_string(last_name))

        try:
            cursor = db.cursor()
            cursor.execute(insert_regular_user)
            db.commit()
            ret_val = User(user_name, None, password, first_name, last_name)
        except IntegrityError:
            db.rollback()
            error = "Username already in use. Please select a different username."
        except:
            db.rollback()
            error = "Unable to create new user please try again later."

        db.close()

        return ret_val, error
