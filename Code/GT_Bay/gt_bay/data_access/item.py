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
            #todo / comment by Joy: if we keep _auction_start_date_time, should we change to
            #now = auction_start_date_time + timedelta(days= int(auction_length))
            now = datetime.now() + timedelta(days= int(auction_length))
            self._auction_end_time = now.strftime('%Y-%m-%d %H:%M:%S')
        else:
            self._auction_end_time = None
        self._get_it_now = get_it_now
        #todo / comment by Joy: do we need _auction_start_date_time?
        self._auction_start_date_time = auction_start_date_time
        self._listing_username = listing_username


    @staticmethod
    def get_item(item_id):
        ret_val = None
        error = None

        get_item_sql = """
        SELECT
          i.item_name,
          i.description,
          c.category_name,
          i.item_condition,
          i.returnable,
          i.get_it_now_price,
          i.auction_end_time,
	  i.listing_username
        FROM Item i INNER JOIN Category c ON i.category_id = c.category_id
        WHERE i.item_id = {item_id};
        """.format(item_id=item_id)

        db = Item.get_db()
        try:
            cursor = db.cursor()
            cursor.execute(get_item_sql)
            ret_val = cursor.fetchone()
            if ret_val is None:
                error = "Item ID {} not found".format(item_id)
            logging.debug("get_item {}".format(ret_val))
        except:
            error = "Unable to connect please try again later."

        return ret_val, error


    @staticmethod
    def get_bids(item_id):
        ret_val = None
        error = None

        get_bids_sql = """
        SELECT
          b.bid_amount,
          b.bid_time,
          u.username
        FROM Bid b INNER JOIN RegularUser u ON b.username = u.username
        WHERE b.item_id = {item_id}
        ORDER BY b.bid_time DESC
        LIMIT 4;
        """.format(item_id=item_id)

        db = Item.get_db()
        try:
            logging.debug("before  cursor.execute(get_bids_sql)")
            cursor = db.cursor(pymysql.cursors.DictCursor)
            cursor.execute(get_bids_sql)
            logging.debug("after  cursor.execute(get_bids_sql)")
            ret_val = cursor.fetchall()
            logging.debug("ret_val {}".format(ret_val))
        except:
            error = "Unable to connect please try again later."
            logging.debug("except {}".format(error))

        db.close()

        return ret_val, error


    @staticmethod
    def get_min_bid(item_id):
        ret_val = None
        error = None

        get_min_sql = """
        SELECT
          IF(IFNULL(max(b.bid_amount),-1) >= i.starting_bid, 
             max(b.bid_amount) + 1,
             i.starting_bid) 
          AS 'min_bid'
        FROM Item i JOIN Bid b ON b.item_id = i.item_id
        WHERE i.item_id = {item_id};
        """.format(item_id=item_id)

        db = Item.get_db()
        try:
            logging.debug("before  cursor.execute(get_min_sql)")
            cursor = db.cursor()
            cursor.execute(get_min_sql)
            logging.debug("after  cursor.execute(get_min_sql)")
            ret_val = cursor.fetchone()
            logging.debug("ret_val {}".format(ret_val))
            if ret_val is None:
                error = "No minimum bid found"
        except:
            error = "Unable to connect please try again later."
            logging.debug("except {}".format(error))

        db.close()

        return ret_val, error


    @staticmethod
    def place_bid(item_id, bid_amount, username):
        ret_val = None
        error = None

        place_bid_sql = """
        INSERT INTO Bid (username, item_id, bid_amount)
        SELECT username, item_id, bid_amount
        FROM BID
        WHERE (SELECT auction_end_time from Item where item_id = {item_id}) > CURRENT_TIMESTAMP
          AND ((SELECT count(*) from Bid where item_id = {item_id}) = 0
               OR (SELECT max(bid_amount) + 1 from Bid where item_id = {item_id}) <= {bid_amount});
        """.format(username=username, item_id=item_id, bid_amount=bid_amount)

        logging.debug("place_bid SQL: {}".format(place_bid_sql))

        db = Item.get_db()
        try:
            cursor = db.cursor()
            cursor.execute(place_bid_sql)
            db.commit()
            ret_val = cursor.rowcount
        except:
            db.rollback()
            error = "Unable to place bid please try again later."

        db.close()

        logging.debug("{} {}".format(ret_val, error))
        return ret_val, error


    @staticmethod
    def get_now(item_id, username):
        ret_val = None
        error = None

        get_now_sql1 = """
        SET @now = CURRENT_TIMESTAMP;
        """

        get_now_sql2 = """
        UPDATE Item
        SET auction_end_time = 
        IF(auction_end_time > @now, 
        @now, auction_end_time)
        WHERE item_id = {item_id};
        """.format(item_id=item_id)

        get_now_sql3 = """
        INSERT INTO Bid 
        (username, item_id, bid_amount, bid_time)
        SELECT 
        '{username}', {item_id}, get_it_now_price, @now
        FROM Item 
        WHERE Item.item_id = {item_id} AND 
              Item.auction_end_time = @now;
        """.format(username=username, item_id=item_id)

        logging.debug("get_now SQL 1: {}".format(get_now_sql1))
        logging.debug("get_now SQL 2: {}".format(get_now_sql2))
        logging.debug("get_now SQL 3: {}".format(get_now_sql3))

        db = Item.get_db()
        try:
            cursor = db.cursor()
            cursor.execute(get_now_sql1)
            cursor.execute(get_now_sql2)
            cursor.execute(get_now_sql3)
            db.commit()
            ret_val = cursor.rowcount
        except:
            db.rollback()
            error = "Unable to purchase please try again later."

        db.close()

        logging.debug("{} {}".format(ret_val, error))
        return ret_val, error


    def persist(self):
        logging.debug("persist item")
        ret_val = None
        error = None

        insert_item="INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, " \
                   "min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username) " \
                   "VALUES ('{}', '{}', {}, {}, {}, {}, {}, DATE_ADD(NOW(), INTERVAL {} DAY) , {}, '{}')".format(
            self._item_name,
            self._description,
            self._item_condition,
            self._returnable,
            self._starting_bid,
            self._minimum_sale,
            self._get_it_now,
            self._auction_length,
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
            ORDER BY auction_end_time;
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

    @staticmethod
    def updateDesc(item_id, desc):
        logging.debug("persist item")
        ret_val = None
        error = None

        updateDesc_sql = """UPDATE Item
                            SET description = '{desc}'
                            WHERE item_id = {item_id};""".format(desc=desc, item_id=item_id)

        logging.debug(updateDesc_sql)
        db = Item.get_db()
        try:
            cursor = db.cursor()
            cursor.execute(updateDesc_sql)
            db.commit()
            ret_val = cursor.lastrowid
        except:
            db.rollback()
            error = "Unable to update item description please try again later."

        db.close()

        return ret_val, error