from data_access.base_data_access_object import BaseDAO
import logging

logger = logging.getLogger()


class Report(BaseDAO):
    def category_report(self):
        ret_val = None
        error = None

        category_report_sql =  """
            SELECT
              c.category_name     AS 'Category',
              count(get_it_now_price) AS 'Total Items',
              min(i.get_it_now_price) AS 'Min Price',
              max(get_it_now_price)   AS 'Max Price',
              avg(get_it_now_price)   AS 'Average Price'
            FROM category c LEFT OUTER JOIN item i ON c.category_id = i.category_id
            GROUP BY c.category_id
            ORDER BY c.category_name;
            """

        db = self.get_db()
        try:
            cursor = db.cursor()
            cursor.execute(category_report_sql)
            db_result = cursor.fetchone()
            if db_result is None:
                error = "Username and or password is incorrect."
            else:
                pass
                #ret_val = User(db_result[0], db_result[1])
                # create report object

            logging.debug("data {}".format(db_result))
        except:
            error = "Unable to connect please try again later."

        db.close()

        return ret_val, error
