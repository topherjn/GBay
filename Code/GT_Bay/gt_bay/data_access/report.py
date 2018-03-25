from data_access.base_data_access_object import BaseDAO
import logging
import pymysql.cursors

logger = logging.getLogger()


class Report(BaseDAO):
    def category_report(self):
        category_report_sql =  """SELECT * FROM Category_Report;"""
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
