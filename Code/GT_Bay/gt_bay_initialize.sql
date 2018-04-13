-- **********************************
-- DDL for cs6400_spr18_team047 DB
-- Sample data
DROP DATABASE cs6400_spr18_team047;
CREATE DATABASE cs6400_spr18_team047;
USE cs6400_spr18_team047;


-- Start fresh delete existing tables
DROP TABLE IF EXISTS Bid;
DROP TABLE IF EXISTS Rating;
DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS AdminUser;
DROP TABLE IF EXISTS RegularUser;
DROP TABLE IF EXISTS Category;
DROP VIEW IF EXISTS CategoryReport;
DROP VIEW IF EXISTS UserReport_Listed;
DROP VIEW IF EXISTS UserReport_Sold;
DROP VIEW IF EXISTS UserReport_Purchased;
DROP VIEW IF EXISTS UserReport_Rated;
DROP VIEW IF EXISTS UserReport_LS;
DROP VIEW IF EXISTS UserReport_LSP;
DROP VIEW IF EXISTS UserReport_LSPR;
DROP VIEW IF EXISTS UserReport;


-- Create the tables
CREATE TABLE Category (
   category_id INT NOT NULL,
   category_name VARCHAR(20) NOT NULL,
   PRIMARY KEY (category_id),
   UNIQUE KEY (category_name)
);


CREATE TABLE RegularUser(
   username VARCHAR(50) NOT NULL,
   password VARCHAR(50) NOT NULL,
   first_name VARCHAR(50) NOT NULL,
   last_name VARCHAR(50) NOT NULL,
   PRIMARY KEY (username)
);


CREATE TABLE AdminUser(
   username VARCHAR(50) NOT NULL,
   position VARCHAR(50) NOT NULL,
   FOREIGN KEY (username) REFERENCES RegularUser(username),
   PRIMARY KEY (username)
);

CREATE TABLE Item(
   item_id INT NOT NULL AUTO_INCREMENT,
   item_name VARCHAR(50) NOT NULL,
   description TEXT NOT NULL,
   item_condition ENUM ('Poor','Fair','Good','Very Good','New') NOT NULL,
   returnable BOOLEAN NOT NULL DEFAULT false,
   starting_bid DECIMAL(10,2) NOT NULL,
   min_sale_price DECIMAL(10,2) NOT NULL CHECK(min_sale_price >= starting_bid),
   get_it_now_price DECIMAL(10,2) NULL CHECK(get_it_now_price >= min_sale_price),
   auction_end_time DATETIME NOT NULL,
   category_id INT NOT NULL,
   listing_username VARCHAR(50) NOT NULL,
   FOREIGN KEY (category_id) REFERENCES Category(category_id),
   FOREIGN KEY (listing_username) REFERENCES RegularUser(username),
   PRIMARY KEY (item_id)
);


CREATE TABLE Rating(
   username VARCHAR(50) NOT NULL,
   item_id INT NOT NULL,
   numstars INT unsigned NOT NULL CHECK(nbr_stars < 6),
   comments TEXT NULL,
   rating_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   FOREIGN KEY (username) REFERENCES RegularUser(username),
   FOREIGN KEY (item_id) REFERENCES Item(item_id),
   PRIMARY KEY (username, item_id)
);


CREATE TABLE Bid(
   username VARCHAR(50) NOT NULL,
   item_id INT NOT NULL,
   bid_amount DECIMAL(10,2) NOT NULL,
   bid_time TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (username) REFERENCES RegularUser(username),
   FOREIGN KEY (item_id) REFERENCES Item(item_id),
   PRIMARY KEY (username, item_id, bid_time)
); 

CREATE VIEW CategoryReport AS
SELECT	  c.category_name     AS 'Category',
                count(i.item_id) AS 'Total Items',
                min(i.get_it_now_price) AS 'Min Price',
                max(get_it_now_price)   AS 'Max Price',
                ROUND(avg(get_it_now_price),2)   AS 'Average Price'
            FROM Category c LEFT OUTER JOIN Item i ON c.category_id = i.category_id
            GROUP BY c.category_id
            ORDER BY c.category_name;

CREATE VIEW UserReport_Listed AS
Select *
FROM
	(
		SELECT listing_username AS username, COUNT(listing_username) AS num_listed
		FROM Item
		GROUP BY listing_username
	) AS ListedT
;

CREATE VIEW UserReport_Sold AS
Select *
FROM
	(
		SELECT listing_username AS username, COUNT(*) AS num_sold
		FROM Bid b1
		  NATURAL JOIN (
			SELECT item_id, max(bid_amount) AS bid_amount
			FROM Bid GROUP BY item_id) AS b2
				NATURAL JOIN Item i
				WHERE auction_end_time < NOW() AND bid_amount >= min_sale_price
		GROUP BY listing_username
	) AS SoldT
;

CREATE VIEW UserReport_Purchased AS
Select *
FROM
	(
		SELECT username AS username, COUNT(*) AS num_purchased
		FROM Bid b1
		NATURAL JOIN (
			SELECT item_id, max(bid_amount) AS bid_amount
			FROM Bid GROUP BY item_id) AS b2
			NATURAL JOIN Item i
			WHERE auction_end_time < NOW() AND bid_amount >= min_sale_price
		GROUP BY username
	) AS PurchasedT
;

CREATE VIEW UserReport_Rated AS
Select *
FROM
	(
		SELECT username AS username, COUNT(username) AS num_rated
		FROM Rating
		GROUP BY username
	) AS RatedT
;


CREATE VIEW UserReport_LS AS
Select *
FROM
	(
        SELECT IFNULL(UserReport_Listed.username, UserReport_Sold.username) AS username, num_listed, num_sold
		FROM
			(
				UserReport_Listed LEFT JOIN UserReport_Sold
				ON UserReport_Listed.username = UserReport_Sold.username
			)

		UNION

        SELECT IFNULL(UserReport_Listed.username, UserReport_Sold.username) AS username, num_listed, num_sold
		FROM
			(
				UserReport_Listed RIGHT JOIN UserReport_Sold
				ON UserReport_Listed.username = UserReport_Sold.username
			)

        ORDER BY num_listed DESC
	) AS ListedSoldT
;


CREATE VIEW UserReport_LSP AS
Select *
FROM
	(
		SELECT IFNULL(UserReport_LS.username, UserReport_Purchased.username) AS username, num_listed, num_sold, num_purchased
		FROM
			(
				UserReport_LS LEFT JOIN UserReport_Purchased
				ON UserReport_LS.username = UserReport_Purchased.username
			)

		UNION

        SELECT IFNULL(UserReport_LS.username, UserReport_Purchased.username) AS username, num_listed, num_sold, num_purchased
		FROM
			(
				UserReport_LS RIGHT JOIN UserReport_Purchased
				ON UserReport_LS.username = UserReport_Purchased.username
			)

        ORDER BY num_listed DESC
	) AS ListedSoldPurchasedT
;


CREATE VIEW UserReport_LSPR AS
Select *
FROM
	(
		SELECT IFNULL(UserReport_LSP.username, UserReport_Rated.username) AS username, num_listed, num_sold, num_purchased, num_rated
		FROM
			(
				UserReport_LSP LEFT JOIN UserReport_Rated
				ON UserReport_LSP.username = UserReport_Rated.username
			)

		UNION

        SELECT IFNULL(UserReport_LSP.username, UserReport_Rated.username) AS username, num_listed, num_sold, num_purchased, num_rated
		FROM
			(
				UserReport_LSP RIGHT JOIN UserReport_Rated
				ON UserReport_LSP.username = UserReport_Rated.username
			)

        ORDER BY num_listed DESC
	) AS ListedSoldPurchasedRatedT
;


CREATE VIEW UserReport AS
Select *
FROM
	(
		SELECT u.username, a.num_listed, a.num_sold, a.num_purchased, a.num_rated
        FROM RegularUser AS u LEFT JOIN UserReport_LSPR AS a
        ON u.username = a.username
        ORDER BY a.num_listed DESC, u.username ASC
	) AS UserReportT
;




-- **********************************
-- Insert category data
INSERT INTO Category(category_id, category_name) VALUES (1, 'Art');
INSERT INTO Category(category_id, category_name) VALUES (2, 'Books');
INSERT INTO Category(category_id, category_name) VALUES (3, 'Electronics');
INSERT INTO Category(category_id, category_name) VALUES (4, 'Home & Garden');
INSERT INTO Category(category_id, category_name) VALUES (5, 'Sporting Goods');
INSERT INTO Category(category_id, category_name) VALUES (6, 'Toys');
INSERT INTO Category(category_id, category_name) VALUES (7, 'Other');

-- Add regular User
INSERT INTO RegularUser(username, password, first_name, last_name) VALUES ('user1', 'pass1', 'Dante', 'Kelor');
INSERT INTO RegularUser(username, password, first_name, last_name) VALUES ('user2', 'pass2', 'Dodra', 'Kiney');
INSERT INTO RegularUser(username, password, first_name, last_name) VALUES ('user3', 'pass3', 'Peran', 'Bishop');
INSERT INTO RegularUser(username, password, first_name, last_name) VALUES ('user4', 'pass4', 'Randy', 'Rorann');
INSERT INTO RegularUser(username, password, first_name, last_name) VALUES ('user5', 'pass5', 'Ashod', 'Iankel');
INSERT INTO RegularUser(username, password, first_name, last_name) VALUES ('user6', 'pass6', 'Cany', 'Achant');
INSERT INTO RegularUser(username, password, first_name, last_name) VALUES ('sell1', 'pass', 'one', 'sell');  -- user report (1 listed, 1 sold)
INSERT INTO RegularUser(username, password, first_name, last_name) VALUES ('ghost', 'pass', 'stealthy', 'watcher');  -- user report (no activity)
INSERT INTO RegularUser(username, password, first_name, last_name) VALUES ('admin1', 'opensesame', 'Riley', 'Fuiss');
INSERT INTO RegularUser(username, password, first_name, last_name) VALUES ('admin2', 'opensesayou', 'Tonnis', 'Kinser');

-- Add an admin user
INSERT INTO AdminUser(username, position) VALUES ('admin1', 'Technical Support');
INSERT INTO AdminUser(username, position) VALUES ('admin2', 'Chief Techy');


-- Items from Piazza 
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
   VALUES ('Garmin GPS', 'This is a great GPS', 3, false, 50.00, 70.00, 99.00,'2018-03-31 12:22', 3, 'user1');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
   VALUES ('Canon Powershot', 'Point and shoot!', 2, false, 40.00, 60.00, 80.00,'2018-04-01 14:14:00', 3, 'user1');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
   VALUES ('Nikon D3', 'New and in box!', 4, false, 1500.00, 1800.00, 2000.00,'2018-04-05 09:19:00', 3, 'user2');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
   VALUES ('Danish Art Book', 'Delicious Danish Art', 3, true, 10.00, 10.00, 10.00,'2018-04-05 15:33:00', 1, 'user3');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
   VALUES ('SQL in 10 Minutes', 'Learn SQL really fast!', 1, false, 5.00, 10.00, 12.00,'2018-04-05 16:48:00', 2, 'admin1');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
   VALUES ('SQL in 8 Minutes', 'Learn SQL even fastter!', 2, false, 5.00, 8.00, 10.00,'2018-04-08 10:01:00', 2, 'admin2');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
   VALUES ('Pull-up Bar', 'Works on any door frame', 4, false, 20.00, 25.00, 40.00,'2018-04-09 22:09:00', 5, 'user6');


-- Items to test ratings
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username) 
	VALUES ('Roomba', 'Autonomously cleans rooms.  Pet version.', 4, false, 100.00, 200.00, 500.00, '2018-01-11', 3, 'user1');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username) 
	VALUES ('Roomba', 'Vacuums by itself.', 3, false, 50.00, 150.00, 450.00, DATE_ADD(NOW(), INTERVAL 3 DAY), 3, 'user1');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username) 
	VALUES ('Roomba', 'Doubles as a cat mount.', 4, true, 250.00, 450.00, NULL, DATE_ADD(NOW(), INTERVAL 7 DAY), 3, 'user2');

-- Items added in order to always have live auctions
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username) 
	VALUES ('Chess', 'Classic ancient board game', 4, false, 20.00, 30.00, 60.00, DATE_ADD(NOW(), INTERVAL 1 DAY), 6, 'user1');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username) 
	VALUES ('Chisel', 'Useful for woodwork', 3, true, 2.00, 5.00, 15.00, DATE_ADD(NOW(), INTERVAL 3 DAY), 4, 'user2');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username) 
	VALUES ('Cricket Bat', 'For your favorite Limey', 1, true, 250.00, 450.00, 650.00, DATE_ADD(NOW(), INTERVAL 5 DAY), 6, 'user3');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username) 
	VALUES ('Candles (1 dozen)', 'For emergencies', 2, true, 1.00, 4.00, 12.00, DATE_ADD(NOW(), INTERVAL 7 DAY), 4, 'user3');

-- Items added for Search
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
	VALUES ('Fountain', 'Just a urinal... Really that it', 5, true, 1.00, 5.00, 10.00, DATE_ADD(NOW(), INTERVAL 7 DAY), 1, 'user6');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
	VALUES ('The Starry Night', 'Widely loved Dutch post-impressionistic landscape', 4, false, 10.00, 50.00, 100.00, DATE_ADD(NOW(), INTERVAL 7 DAY), 1, 'user6');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
	VALUES ('Guernica', 'Large Spanish oil painting depicting the horrors of war', 3, false, 100.00, 500.00, 1000.00, DATE_ADD(NOW(), INTERVAL 7 DAY), 1, 'user6');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
	VALUES ('Sagrada Familia', 'Sure it\'s not yet complete, but this Spanish wonder is an absolute steal!', 4, false, 250.00, 1000.00, 10000.00, DATE_ADD(NOW(), INTERVAL 7 DAY), 1, 'user6');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
	VALUES ('The Creation of Man', 'Sistine Chapel ceiling excerpt', 2, false, 1000.00, 5000.00, 1000000.00, DATE_ADD(NOW(), INTERVAL 7 DAY), 1, 'user6');

-- Items added for User Report
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
	VALUES ('One Hit Wonder', 'You only have to do it really well once.', 5, false, 1.00, 2.50, 10.00, DATE_ADD(NOW(), INTERVAL 7 DAY), 6, 'sell1');

-- Newer seed data
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
   VALUES ('Garmin GPS', 'Typical GPS unit', 2, false, 25.00, 50.00, 75.00,'2018-04-23 03:15', 3, 'admin2');

INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
   VALUES ('MacBook Pro', 'Fanboy favorite', 4, false, 1000.00, 1500.00, NULL,'2018-04-23 01:01', 3, 'user4');

INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
   VALUES ('Microsoft Surface', 'Listed only to compare unfavorably to the Apple cult', 3, false, 500.00, 750.00, 899.00, '2018-04-23 06:00', 3, 'user5');

-- Ratings from Piazza
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user2', 1, 5, 'Great GPS!');
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user3', 1, 2, 'Not so great GPS!');
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user4', 1, 4, 'A favorite of mine.');
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user1', 4, 1, 'Go for the italian stuff instead.');
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('admin1', 6, 1, 'Not recommended.');
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user1', 6, 3, 'This book is okay.');
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user2', 6, 5, 'I learned SQL in 8 minutes!');

-- Ratings test ratings
INSERT INTO Rating(username, item_id, numstars, comments, rating_time) VALUES ('user1', 8, 3, 'Cleans OK but needs cleaning itself a lot','2018-01-04');
INSERT INTO Rating(username, item_id, numstars, comments, rating_time) VALUES ('user2', 8, 5, 'I love this gadget!','2018-04-01');
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user3', 8, 0, 'Lasted one week before it broke');

-- Ratings from seed data
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user5',22, 3, 'Great for getting OMSCS coursework done.');
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user4',23, 2, 'Looks nice but but underpowered.');
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user3',23, 3, NULL);

-- Bids from Piazza
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user4', 1, 50.00, '2018-03-30 14:53');
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user5', 1, 55.00, '2018-03-30 16:45');
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user4', 1, 75.00, '2018-03-30 16:45');
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user5', 1, 85.00, '2018-03-31 10:45');
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user6', 2, 80.00, '2018-04-01 13:55');
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user1', 3, 1500.00, '2018-04-04 08:37');
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user3', 3, 1501.00, '2018-04-04 09:25');
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user1', 3, 1795.00, '2018-04-04 12:27');
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user4', 7, 20.00, '2018-04-04 20:20');
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user2', 7, 25.00, '2018-04-09 21:15');


-- Bid from seed data
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user4', 21, 30.00, '2018-04-17 14:00');
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user5', 21, 31.00, '2018-04-17 20:00');
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user3', 21, 33.00, '2018-04-18 01:00');
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user4', 21, 40.00, '2018-04-18 06:00');
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user6', 21, 45.00, '2018-04-18 14:00');

-- Bids added for Search
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user4', 16, 10.00, NOW());
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user4', 17, 101.00, NOW());
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user1', 18, 250.00, NOW());
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user2', 19, 1000.00, NOW());
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user3', 19, 2000.00, NOW());

