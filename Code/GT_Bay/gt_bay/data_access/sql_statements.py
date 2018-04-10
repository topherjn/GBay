class SQLStatements(object):
    """This class aggregates all of the app's SQL for grading convenience.
    """



    ##### category: START
    # get all categories
    get_categories = """SELECT category_id, category_name FROM Category ORDER BY category_id;"""
    ##### category: END


    ##### user.py: START
    # attempt to get user (and admin position if user is an admin) based on username and password
    select_gt_bay_user = """SELECT RegularUser.username, AdminUser.position 
                            FROM RegularUser LEFT JOIN AdminUser ON RegularUser.username = AdminUser.username 
                            WHERE RegularUser.username = '{}' AND RegularUser.password = '{}';"""

    # registers new user
    insert_regular_user = """INSERT INTO RegularUser(username, password, first_name, last_name) 
                          VALUES ('{}', '{}', '{}', '{}');"""
    ##### user.py: END


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
