from data_access.base_data_access_object import BaseDAO
import logging
import pymysql.cursors

logger = logging.getLogger()


class Report(BaseDAO):
    def category_report(self):
        category_report_sql =  """
            SELECT	  c.category_name     AS 'Category',
                count(get_it_now_price) AS 'Total Items',
                min(i.get_it_now_price) AS 'Min Price',
                max(get_it_now_price)   AS 'Max Price',
                ROUND(avg(get_it_now_price),2)   AS 'Average Price'
            FROM Category c LEFT OUTER JOIN Item i ON c.category_id = i.category_id
            GROUP BY c.category_id
            ORDER BY c.category_name;
            """

        ret_val = None
        error = None

        db = Report.get_db()
        try:

            cursor = db.cursor(pymysql.cursors.DictCursor)
            cursor.execute(category_report_sql)
            ret_val = cursor.fetchall()
            if ret_val is None:
                error = "Username and or password is incorrect."
            logging.debug("data {}".format(ret_val))

        except:
            error = "Unable to connect please try again later."

        db.close()

        return ret_val, error
