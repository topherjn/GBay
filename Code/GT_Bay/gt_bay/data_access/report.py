from data_access.base_data_access_object import BaseDAO
from data_access.sql_statements import SQLStatements
import logging
import pymysql.cursors

logger = logging.getLogger()


class Report(BaseDAO):

    @staticmethod
    def auction_results():
        auction_results_sql = SQLStatements.auction_results
        ret_val = None
        error = None

        db = Report.get_db()
        try:
            logging.debug("before  cursor.execute(auction_results_sql)")
            cursor = db.cursor(pymysql.cursors.DictCursor)
            cursor.execute(auction_results_sql)
            logging.debug("after  cursor.execute(auction_results_sql)")
            ret_val = cursor.fetchall()
            logging.debug("ret_val {}".format(ret_val))
        except:
            error = "Unable to connect please try again later"
            logging.debug("except {}".format(error))

        db.close()

        return ret_val, error

    def category_report(self):
        category_report_sql = SQLStatements.category_report
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

    def user_report(self):
        user_report_sql = SQLStatements.user_report
        ret_val = None
        error = None

        db = Report.get_db()
        try:

            cursor = db.cursor(pymysql.cursors.DictCursor)
            cursor.execute(user_report_sql)
            ret_val = cursor.fetchall()
            if ret_val is None:
                error = "Username and or password is incorrect."
            logging.debug("data {}".format(ret_val))

        except:
            error = "Unable to connect please try again later."

        db.close()

        return ret_val, error
