import logging
from datetime import datetime
from datetime import timedelta

from pymysql import IntegrityError
import pymysql.cursors

from data_access.base_data_access_object import BaseDAO

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Item(BaseDAO):
    def __init__(self, item_id=None, item_name=None, description=None, category_id=None,
                 item_condition=None, returnable=None,
                 starting_bid=None, minimum_sale=None, auction_length=None,
                 auction_start_date_time=None, listing_username=None, get_it_now=None):
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
        if auction_length is not None:
            now = datetime.now() + timedelta(days= int(auction_length))
            self._auction_end_time = now.strftime('%Y-%m-%d %H:%M:%S')
        else:
            self._auction_end_time = None
        self._get_it_now = get_it_now
        self._auction_start_date_time = auction_start_date_time
        self._listing_username = listing_username


    def get_item(self, item_id):
        ret_val = None
        error = None

        get_item_sql = """
        SELECT
          i.item_name,
          i.description,
          c.category_name,
          i.item_condition,
          i.get_it_now_price,
          i.returnable,
          i.auction_end_time
        FROM Item i INNER JOIN Category c ON i.category_id = c.category_id
        WHERE i.item_id = {item_id};
        """.format(item_id=item_id)

        db = Item.get_db()
        try:
            cursor = db.cursor()
            cursor.execute(get_item_sql)
            ret_val = cursor.fetchone()
            if ret_val is None:
                error = "Item ID not found"

            logging.debug("get_item {}".format(ret_val))
        except:
            error = "Unable to connect please try again later."

        return ret_val, error


    def persist(self):
        logging.debug("persist item")
        ret_val = None
        error = None

        insert_item="INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, " \
                   "min_sale_price, get_it_now_price, auction_length, auction_end_time, category_id, listing_username) " \
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

    def search(self, key_word, category, minPrice, maxPrice, conditionAtLeast):
        search_sql = """
            SELECT
              Item.item_id,
              item_name,
              bid_amount AS current_bid,
              username   AS high_bidder,
              get_it_now_price,
              auction_end_time
            FROM Item
              INNER JOIN Category
                ON Item.category_id = Category.category_id
              LEFT JOIN
              (SELECT
                 item_id,
                 bid_amount,
                 username
               FROM Bid b1 NATURAL JOIN
                 (SELECT
                    item_id,
                    max(bid_amount) AS bid_amount
                  FROM Bid
                  GROUP BY item_id) AS b2)
                AS CurrentBid
                ON Item.item_id = CurrentBid.item_id
            WHERE auction_end_time > NOW()
                  AND (item_name LIKE CONCAT('%', '{key_word}', '%')
                       OR description LIKE CONCAT('%', '{key_word}', '%'))
                  AND ({category} IS NULL OR {category} = 0
                       OR Item.category_id = {category})
                  AND ({minPrice} IS NULL OR
                       IF(bid_amount IS NULL, starting_bid, bid_amount)
                       >= {minPrice})
                  AND ({maxPrice} IS NULL OR
                       IF(bid_amount IS NULL, starting_bid, bid_amount)
                       <= {maxPrice})
                  AND ({conditionAtLeast} IS NULL OR
                       item_condition >= {conditionAtLeast})
            ORDER BY auction_end_time
        """.format(key_word=key_word, category=category, minPrice=minPrice,
                   maxPrice=maxPrice, conditionAtLeast=conditionAtLeast)

        logging.debug("SQL [{}]".format(search_sql))
        ret_val = None
        error = None

        db = self.get_db()
        try:
            logging.debug("before  cursor.execute(search_sql)")
            cursor = db.cursor(pymysql.cursors.DictCursor)
            cursor.execute(search_sql)
            logging.debug("after  cursor.execute(search_sql)")
            ret_val = cursor.fetchall()
            logging.debug("ret_val {}".format(ret_val))
            if ret_val is None:
                error = "No results found"

            logging.debug("data {}".format(ret_val))
        except:
            error = "Unable to connect please try again later."
            logging.debug("except {}".format(error))

        db.close()

        return ret_val, error




