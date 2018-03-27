import logging

from pymysql import IntegrityError

from data_access.base_data_access_object import BaseDAO

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Category(BaseDAO):

    @staticmethod
    def get_categories():
        category_choices=[]
        error = None
        logging.debug("get_categories")

        select_sql = "SELECT category_id, category_name FROM Category ORDER BY category_id"

        db = Category.get_db()
        try:
            cursor = db.cursor()
            cursor.execute(select_sql)

            results = cursor.fetchall()

            for row in results:
                category_choices.append((row[0], row[1]))
        except:
            error = "Unable to connect please try again later."

        return category_choices, error

