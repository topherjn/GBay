import logging
from datetime import datetime
from datetime import timedelta

from pymysql import IntegrityError

from data_access.base_data_access_object import BaseDAO

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Item(BaseDAO):
    def __init__(self, item_id, item_name, description, category_id, item_condition, returnable,
                 starting_bid, minimum_sale, auction_length,
                 auction_start_date_time, listing_username, get_it_now=None):
        logging.debug("in constructor")
        self._item_id = item_id
        self._item_name = item_name
        self._description = description
        self._category_id = category_id
        self._item_condition = item_condition
        self._returnable = returnable
        self._starting_bid = starting_bid
        self._minimum_sale = minimum_sale
        self._auction_length = auction_length
        now = datetime.now() + timedelta(days= int(auction_length))
        self._auction_end_time = now.strftime('%Y-%m-%d %H:%M:%S')
        self._get_it_now = get_it_now
        self._auction_start_date_time = auction_start_date_time
        self._listing_username = listing_username


    def persist(self):
        logging.debug("persist item")
        ret_val = None
        error = None

        insert_item="INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, " \
                   "minimum_sale, get_it_now, auction_length, auction_end_time, category_id, listing_username) " \
                   "VALUES ('{}', '{}', {}, {}, {}, {}, {}, {}, '{}', {}, '{}')".format(
            self._item_name,
            self._description,
            self._item_condition,
            self._returnable,
            self._starting_bid,
            self._minimum_sale,
            self._get_it_now,
            self._auction_length,
            self._auction_end_time,
            self._category_id,
            self._listing_username)

        logging.debug(insert_item)
        db = self.get_db()
        try:
            cursor = db.cursor()
            cursor.execute(insert_item)
            db.commit()
            ret_val = cursor.lastrowid
        except:
            db.rollback()
            error = "Unable to create item please try again later."

        db.close()

        return ret_val, error



