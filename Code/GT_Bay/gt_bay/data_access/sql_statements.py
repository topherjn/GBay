class SQLStatements(object):
    """This class aggregates all of the app's SQL for grading convenience.
    """



    ##### category: START
    # get all categories
    get_categories = """SELECT category_id, category_name FROM Category ORDER BY category_id;"""
    ##### category: END


    ##### item.py: START
    # x
    get_item = """
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
    """

    # x
    get_bids = """
        SELECT
          b.bid_amount,
          b.bid_time,
          u.username
        FROM Bid b INNER JOIN RegularUser u ON b.username = u.username
        WHERE b.item_id = {item_id}
        ORDER BY b.bid_time DESC
        LIMIT 4;
    """

    # x
    get_min = """
        SELECT
          IF(IFNULL(max(b.bid_amount),-1) >= i.starting_bid, 
             max(b.bid_amount) + 1,
             i.starting_bid) 
          AS 'min_bid'
        FROM Item i JOIN Bid b ON b.item_id = i.item_id
        WHERE i.item_id = {item_id};
    """

    # x
    place_bid = """
        INSERT INTO Bid (username, item_id, bid_amount)
        SELECT '{username}', {item_id}, {bid_amount}
        WHERE (SELECT auction_end_time from Item where item_id = {item_id}) > CURRENT_TIMESTAMP
          AND ((SELECT count(*) from Bid where item_id = {item_id}) = 0
               OR (SELECT max(bid_amount) + 1 from Bid where item_id = {item_id}) <= {bid_amount});
    """

    # x
    get_now_1 = """SET @now = CURRENT_TIMESTAMP;"""

    # x
    get_now_2 = """
        UPDATE Item
        SET auction_end_time = 
        IF(auction_end_time > @now, 
        @now, auction_end_time)
        WHERE item_id = {item_id};
    """

    # x
    get_now_3 = """
        INSERT INTO Bid 
        (username, item_id, bid_amount, bid_time)
        SELECT 
        '{username}', {item_id}, get_it_now_price, @now
        FROM Item 
        WHERE Item.item_id = {item_id} AND 
              Item.auction_end_time = @now;
    """

    # x
    insert_item = """
      INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, " \
      "min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username) " \
      "VALUES ('{}', '{}', {}, {}, {}, {}, {}, DATE_ADD(NOW(), INTERVAL {} DAY) , {}, '{}')
    """

    # x
    search = """
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
    """

    # x
    update_desc = """
        UPDATE Item
        SET description = '{desc}'
        WHERE item_id = {item_id};
    """
    ##### item.py: END


    ##### rating.py: START
    # get item ratings by item_id
    get_rating = """
      SELECT r.username, r.numstars, r.rating_time, r.comments, i.item_name, i.item_id
      FROM Rating r INNER JOIN Item i ON i.item_id = r.item_id WHERE item_name = 
      (SELECT item_name FROM Item WHERE item_id = {item_id}) ORDER BY r.rating_time DESC;
    """

    # get / calculate the rating for item by item_id
    get_avg_rating = """
        SELECT AVG(numstars)
        FROM Rating r inner join Item i on r.item_id = i.item_id
        WHERE item_name = (SELECT item_name FROM Item WHERE item_id = {item_id});
    """

    # check if user has already rated an item by item_id
    check_already_exists = """
        SELECT r.username, i.item_name
        FROM Rating r INNER JOIN Item i ON r.item_id = i.item_id
        WHERE r.username = '{}' AND i.item_name = '{}';
    """

    # save rating by item id
    save_rating = """INSERT INTO Rating(username,item_id,numstars,comments) VALUES ('{}','{}','{}','{}');"""

    # delete rating by item_id
    delete_rating = """DELETE FROM Rating WHERE item_id = '{}' AND username = '{}';"""
    ##### rating.py: END


    ##### report.py: START
    # get data for the Auction Results report
    auction_results = """
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

    # get data for the Category Report
    category_report = """SELECT * FROM CategoryReport;"""

    # get data for the User Report
    user_report = """SELECT * FROM UserReport;"""
    ##### report.py: END


    ##### user.py: START
    # attempt to get user (and admin position if user is an admin) based on username and password
    select_gt_bay_user = """SELECT RegularUser.username, AdminUser.position 
                                FROM RegularUser LEFT JOIN AdminUser ON RegularUser.username = AdminUser.username 
                                WHERE RegularUser.username = '{}' AND RegularUser.password = '{}';"""

    # registers new user
    insert_regular_user = """INSERT INTO RegularUser(username, password, first_name, last_name) 
                              VALUES ('{}', '{}', '{}', '{}');"""
    ##### user.py: END
