import logging
from datetime import datetime
from datetime import timedelta

from pymysql import IntegrityError
import pymysql.cursors

from data_access.base_data_access_object import BaseDAO
from data_access.sql_statements import SQLStatements

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Rating(BaseDAO):

    def __init__(self,username=None,item_id=None,item_name=None,numstars=None,comments=None):

        logging.debug("in rating constructor")
        self._username = username
        self._itemid = item_id
        self._item_name = item_name
        self._numstars = numstars
        self._comments = comments

    def get_rating(self, item_id):
        logging.debug(item_id)
        get_rating_sql = SQLStatements.get_rating.format(item_id=item_id)

        logging.debug(get_rating_sql)
        ret_val = None
        error = None
        
        db = Rating.get_db()
        try:

            cursor = db.cursor(pymysql.cursors.DictCursor)
            cursor.execute(get_rating_sql)
            ret_val = cursor.fetchall()

            logging.debug("get_rating {}".format(ret_val))
        except:
            error = "No ratings yet. Would you like to leave one?"

        logging.debug(ret_val)


        return ret_val, error

    def get_average_rating(self, item_id):
        get_avg_rating_sql = SQLStatements.get_avg_rating.format(item_id=item_id)

        logging.debug(get_avg_rating_sql)

        ret_val = None
        error = None

        db = Rating.get_db()
        try:

            cursor = db.cursor(pymysql.cursors.DictCursor)
            cursor.execute(get_avg_rating_sql)
            ret_val = cursor.fetchone()
            if ret_val is None:
                error = "Average rating not found"

            logging.debug("get_avg_rating {}".format(ret_val))
        except:
            error = "Unable to connect please try again later."

        logging.debug(ret_val)


        return ret_val, error

    def persist(self):
        logging.debug("persist rating")
        ret_val = None
        error = None

        check_already_exists_sql = SQLStatements.check_already_exists.format(self._username,self._item_name)

        logging.debug(check_already_exists_sql)

        db = Rating.get_db()
        try:

            cursor = db.cursor(pymysql.cursors.DictCursor)
            cursor.execute(check_already_exists_sql)
            ret_val = cursor.fetchall()
            if ret_val is not None:
                error = "You already rated this item."

        except:
            error = "Unable to connect please try again later."

        logging.debug("already exists?")
        logging.debug(ret_val)

        if self._numstars is None:
            self._numstars = 0

        if len(ret_val) < 1:
            save_rating_sql = SQLStatements.save_rating.format(
                self._username,
                self._itemid,
                self._numstars,
                db.escape_string(self._comments))

            logging.debug(save_rating_sql)

            db = self.get_db()
            try:
                cursor =db.cursor()
                cursor.execute(save_rating_sql)
                db.commit()
                ret_val = cursor.lastrowid
            except:
                db.rollback()
                error = "Unable to save rating.  Please try again later"
            
            db.close()

        return ret_val, error

    def delete_rating(self,username,item_id):
        delete_rating_sql = SQLStatements.delete_rating.format(item_id=item_id,username=username)

        ret_val = None
        error = None

        logging.debug(delete_rating_sql)

        db = self.get_db()
        try:
            cursor = db.cursor()
            cursor.execute(delete_rating_sql)
            db.commit()
            ret_val = cursor.lastrowid
        except:
            db.rollback()
            error = "Unable to delete rating."

        db.close()

        logging.debug("Delete Rating retval: ")
        logging.debug(ret_val)

        return ret_val, error