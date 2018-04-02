from data_access.base_data_access_object import BaseDAO
import logging
import pymysql.cursors

logger = logging.getLogger()


class Report(BaseDAO):

    @staticmethod
    def auction_results():
        ret_val = None
        error = None

        auction_results_sql = """
        SELECT
          i.item_id,
          i.item_name,
          IF(b.max_bid >= i.min_sale_price, b.max_bid, NULL) AS max_bid,
          IF(b.max_bid >= i.min_sale_price, b.username, NULL) AS username,
          i.auction_end_time
        FROM Item i
          LEFT JOIN (
            -- Select the highest bid amounts for all auctions
            SELECT item_id, bid_amount AS max_bid, username
            FROM Bid b1 NATURAL JOIN
            (SELECT item_id, max(bid_amount) AS bid_amount
            FROM Bid GROUP BY item_id) AS b2      
          ) b ON b.item_id = i.item_id
        WHERE i.auction_end_time < CURRENT_TIMESTAMP
        ORDER BY i.auction_end_time DESC;
        """

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
        category_report_sql =  """SELECT * FROM CategoryReport;"""
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
