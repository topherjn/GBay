import logging
from datetime import datetime
from datetime import timedelta

from pymysql import IntegrityError
import pymysql.cursors

from data_access.base_data_access_object import BaseDAO

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Rating(BaseDAO):

    def get_rating(self, item_id):
        get_rating_sql =  """
            SELECT username AS ratingUsername, numstars, rating_time, comments
            FROM Rating
            WHERE item_id = {item_id}
            ORDER BY rating_time DESC;
            """

        ret_val = None
        error = None

        db = Rating.get_db()
        try:

            cursor = db.cursor(pymysql.cursors.DictCursor)
            cursor.execute(get_rating_sql)
            ret_val = cursor.fetchone()
            if ret_val is None:
                error = "Rating not found"

            logging.debug("get_rating {}".format(ret_val))
        except:
            error = "Unable to connect please try again later."

        return ret_val, error


