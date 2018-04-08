class SQLStatements(object):
    select_gt_bay_user = """SELECT RegularUser.username, AdminUser.position 
                            FROM RegularUser LEFT JOIN AdminUser ON RegularUser.username = AdminUser.username 
                            WHERE RegularUser.username = '{}' AND RegularUser.password = '{}'"""

    insert_regular_user = """INSERT INTO RegularUser(username, password, first_name, last_name) 
                          VALUES ('{}', '{}', '{}', '{}')"""

    user_report = """
        SELECT username_t1 as username, num_listed, num_sold, num_purchased, num_rated
        FROM
    
        (
            (
                SELECT listing_username AS username_t1, COUNT(listing_username) AS num_listed, num_sold
                FROM Item
                    NATURAL JOIN (
                        SELECT listing_username, COUNT(*) AS num_sold
                        FROM Bid AS b1
                            NATURAL JOIN (
                                SELECT item_id, max(bid_amount) AS bid_amount 
                                FROM Bid GROUP BY item_id
                            ) AS b2
                                NATURAL JOIN Item i
                                WHERE auction_end_time < NOW() AND bid_amount >= min_sale_price
                        GROUP BY listing_username
                    ) AS Sold
                GROUP BY username_t1
            ) AS T1
            
            LEFT JOIN
            
            (
                SELECT username AS username_t2, num_purchased, COUNT(username) AS num_rated
                FROM Rating
                    NATURAL JOIN (
                        SELECT username, COUNT(*) AS num_purchased
                        FROM Bid b1
                            NATURAL JOIN (
                                SELECT item_id, max(bid_amount) AS bid_amount 
                                FROM Bid GROUP BY item_id) AS b2
                                    NATURAL JOIN Item i
                                    WHERE auction_end_time < NOW() AND bid_amount >= min_sale_price
                        GROUP BY username
                    ) AS Rated
                GROUP BY username_t2
            ) AS T2
            
            ON username_t1 = username_t2
        )
    
        UNION
        
        SELECT username_t2 as username, num_listed, num_sold, num_purchased, num_rated
        FROM
            (
                (
                    SELECT listing_username AS username_t1, COUNT(listing_username) AS num_listed, num_sold
                    FROM Item
                        NATURAL JOIN (
                            SELECT listing_username, COUNT(*) AS num_sold
                            FROM Bid AS b1
                                NATURAL JOIN (
                                    SELECT item_id, max(bid_amount) AS bid_amount 
                                    FROM Bid GROUP BY item_id
                                ) AS b2
                                    NATURAL JOIN Item i
                                    WHERE auction_end_time < NOW() AND bid_amount >= min_sale_price
                            GROUP BY listing_username
                        ) AS Sold
                    GROUP BY username_t1
                ) AS T3
                
                RIGHT JOIN
                
                (
                    SELECT username AS username_t2, num_purchased, COUNT(username) AS num_rated
                    FROM Rating
                        NATURAL JOIN (
                            SELECT username, COUNT(*) AS num_purchased
                            FROM Bid b1
                                NATURAL JOIN (
                                    SELECT item_id, max(bid_amount) AS bid_amount 
                                    FROM Bid GROUP BY item_id) AS b2
                                        NATURAL JOIN Item i
                                        WHERE auction_end_time < NOW() AND bid_amount >= min_sale_price
                            GROUP BY username
                        ) AS Rated
                    GROUP BY username_t2
                ) AS T4
                
                ON username_t1 = username_t2
            )
        
        ORDER BY num_listed DESC;
    """
