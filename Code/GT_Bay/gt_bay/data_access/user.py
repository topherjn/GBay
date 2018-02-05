import logging
import MySQLdb
from MySQLdb import IntegrityError

from data_access.base_data_access_object import BaseDAO

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class User(BaseDAO):
    def __init__(self, user_id, user_name, password, first_name, last_name, is_admin=False, position=None):
        self._id = user_id
        self._user_name = user_name
        self._password = password
        self._position = position
        self._is_admin = is_admin
        self._first_name = first_name
        self._last_name = last_name

    @property
    def user_name(self):
        return self._user_name

    @property
    def password(self):
        return self._password

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def is_admin(self):
        return self._is_admin

    def to_json(self):
        dict = {'user_id':self._id, 'user_name': self._user_name, 'position': self._position}
        return dict


    @staticmethod
    def login(user_name=None, password=None):
        ret_val = None
        error = None
        logging.debug("sss user_name={}, password={}".format(user_name, password))
        select_sql = "SELECT * FROM GT_BAY_USER WHERE username='{}' AND password='{}'".format(user_name, password)

        db = User.get_db()
        try:
            cursor = db.cursor()
            cursor.execute(select_sql)
            db_result = cursor.fetchone()
            if db_result is None:
                error = "Username and or password is incorrect."
            else:
                ret_val = User(db_result[0], db_result[1], db_result[2], db_result[3],
                               db_result[4], db_result[5], db_result[6])

            logging.debug("data {}".format(db_result))
        except:
            error = "Unable to connect please try again later."

        return ret_val, error

    @staticmethod
    def register_user(user_name=None, password=None, first_name=None, last_name=None):
        ret_val = None
        error = None
        logging.debug("sss user_name={}, password={}".format(user_name, password))

        insert_sql="INSERT INTO GT_BAY_USER(username, password, first_name, last_name) " \
                   "VALUES ('{}', '{}', '{}', '{}')".format(user_name, password, first_name, last_name)

        db = User.get_db()
        try:
            cursor = db.cursor()
            cursor.execute(insert_sql)
            db.commit()
            ret_val = User(cursor.lastrowid, user_name, password, first_name, last_name)
        except IntegrityError:
            db.rollback()
            error = "Username already in use. Please select a different username."
        except:
            db.rollback()
            error = "Unable to create new user please try again later."

        db.close()

        return ret_val, error
