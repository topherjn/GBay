import logging
from datetime import datetime
from datetime import timedelta

from pymysql import IntegrityError
import pymysql.cursors

from data_access.base_data_access_object import BaseDAO

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Rating(BaseDAO):

    def __init__(self,username=None,item_id=None,numstars=None,comments=None):

        logging.debug("in rating constructor")
        self._username = username
        self._item_name = item_id
        self._numstars = numstars
        self._comments = comments

    def get_rating(self, item_id):
        logging.debug(item_id)
        get_rating_sql =  """
            SELECT r.username, r.numstars, r.rating_time, r.comments, r.rating_time, i.item_name
            FROM Rating r INNER JOIN Item i ON i.item_id = r.item_id WHERE item_name = 
            (SELECT item_name FROM Item WHERE item_id = {item_id})
            """.format(item_id=item_id)

        logging.debug(get_rating_sql)
        ret_val = None
        error = None
        
        db = Rating.get_db()
        try:

            cursor = db.cursor(pymysql.cursors.DictCursor)
            cursor.execute(get_rating_sql)
            ret_val = cursor.fetchall()
            if ret_val is None:
                error = "Rating not found"

            logging.debug("get_rating {}".format(ret_val))
        except:
            error = "Unable to connect please try again later."

        logging.debug(ret_val)


        return ret_val, error

    def get_average_rating(self, item_id):
        get_avg_rating_sql = """
                    SELECT AVG(numstars)
                    FROM Rating
                    WHERE item_id = {item_id}
                    """.format(item_id=item_id)
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

        save_rating_sql = """
        INSERT INTO Rating(username,item_id,numstars,comments) VALUES ('{}','{}','{}','{}')""".format(
            self._username,
            self._item_name,
            self._numstars,
            self._comments)
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


