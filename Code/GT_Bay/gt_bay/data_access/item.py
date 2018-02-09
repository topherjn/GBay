import logging

from pymysql import IntegrityError

from data_access.base_data_access_object import BaseDAO

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Item(BaseDAO):
    def __init__(self, item_id, item_name, description, category_id, item_condition, returnable,
                 starting_bid, minimum_sale, auction_length, get_it_now,
                 auction_start_date_time, listing_user_id):
        self._item_id = item_id
        self._item_name = item_name
        self._description = description
        self._category_id = category_id
        self._item_condition = item_condition
        self._returnable = returnable
        self._starting_bid = starting_bid
        self._minimum_sale = minimum_sale
        self._auction_length = auction_length
        self._get_it_now = get_it_now
        self._auction_start_date_time = auction_start_date_time
        self._listing_user_id = listing_user_id


    def persist(self):
        logging.debug("persist item")
        ret_val = None
        error = None

        insert_sql="INSERT INTO ITEM(item_name, description, item_condition, returnable, starting_bid, " \
                   "minimum_sale, get_it_now, auction_length, category_id, listing_user_id) " \
                   "VALUES ('{}', '{}', {}, {}, {}, {}, {}, {}, {}, {})".format(
            self._item_name,
            self._description,
            self._item_condition,
            self._returnable,
            self._starting_bid,
            self._minimum_sale,
            self._get_it_now,
            self._auction_length,
            self._category_id,
            self._listing_user_id)


        db = self.get_db()
        try:
            cursor = db.cursor()
            cursor.execute(insert_sql)
            db.commit()
        except:
            db.rollback()
            error = "Unable to create item please try again later."

        db.close()

        return ret_val, error



