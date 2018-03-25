-- **********************************
-- DDL for cs6400_spr18_team047 DB

-- CREATE DATABASE cs6400_spr18_team047;
USE cs6400_spr18_team047;


-- Start fresh delete existing tables
DROP TABLE IF EXISTS Bid;
DROP TABLE IF EXISTS Rating;
DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS AdminUser;
DROP TABLE IF EXISTS RegularUser;
DROP TABLE IF EXISTS Category;
DROP VIEW IF EXISTS Category_Report;


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
   auction_length INT NOT NULL CHECK(auction_length = 1 or auction_length = 3 or auction_length = 5 or auction_length = 7),
   get_it_now_price DECIMAL(10,2) NULL CHECK(get_it_now_price >= min_sale_price),
   auction_end_time TIMESTAMP NOT NULL CHECK(TIMESTAMP > CURRENT_TIMESTAMP),
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

CREATE VIEW AS Category_Report
SELECT	  c.category_name     AS 'Category',
                count(get_it_now_price) AS 'Total Items',
                min(i.get_it_now_price) AS 'Min Price',
                max(get_it_now_price)   AS 'Max Price',
                ROUND(avg(get_it_now_price),2)   AS 'Average Price'
            FROM Category c LEFT OUTER JOIN Item i ON c.category_id = i.category_id
            GROUP BY c.category_id
            ORDER BY c.category_name;


-- **********************************
-- Insert category data
INSERT INTO Category(category_id, category_name) VALUES (1, 'Art');
INSERT INTO Category(category_id, category_name) VALUES (2, 'Books');
INSERT INTO Category(category_id, category_name) VALUES (3, 'Electronics');
INSERT INTO Category(category_id, category_name) VALUES (4, 'Home and Garden');
INSERT INTO Category(category_id, category_name) VALUES (5, 'Sports Goods');
INSERT INTO Category(category_id, category_name) VALUES (6, 'Toys');
INSERT INTO Category(category_id, category_name) VALUES (7, 'Other');

-- Add an admin user
INSERT INTO RegularUser(username, password, first_name, last_name) VALUES ('admin01', 'password', 'Pierre', 'Omidyar');
INSERT INTO AdminUser(username, position) VALUES ('admin01', 'DBA');

-- Add regular User
INSERT INTO RegularUser(username, password, first_name, last_name) VALUES ('user01', 'password', 'Dan', 'Smith');
INSERT INTO RegularUser(username, password, first_name, last_name) VALUES ('user02', 'password', 'Amy', 'Smith');
INSERT INTO RegularUser(username, password, first_name, last_name) VALUES ('user03', 'password', 'Anne', 'Smith');

INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_length, auction_end_time, category_id, listing_username)
   VALUES ('clock radio', 'digital clock radio', 5, false, 15.00, 20.00, 30.00, 5, '2018-03-06 09:01:52', 3, 'user02');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_length, auction_end_time, category_id, listing_username)
   VALUES ('moby dick', 'classic book', 5, false, 10.00, 15.00, 20.00, 3, '2018-03-03 09:01:52', 2, 'user03');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_length, auction_end_time, category_id, listing_username)
   VALUES ('ipod classic', 'like new ipod', 4, false, 15.00, 20.00, 30.00, 5, '2018-03-06 09:01:52', 3, 'user02');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_length, auction_end_time, category_id, listing_username)
   VALUES ('fishing boat', '12 foot fishing boat', 3, false, 150.00, 200.00, 300.00, 5, '2018-03-06 09:01:52', 5, 'user03');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_length, auction_end_time, category_id, listing_username)
   VALUES ('clock radio', 'digital clock radio', 4, false, 16.00, 21.00, 31.00, 5, '2018-03-06 09:01:52', 3, 'user03');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_length, auction_end_time, category_id, listing_username)
   VALUES ('surfboard', 'retro board', 4, false, 160.00, 210.00, NULL, 5, '2018-03-06 09:01:52', 3, 'user03');


INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user02', 1, 5, 'great product');
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user03', 1, 3, 'its ok alarm to quiet');
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user03', 2, 3, 'to long');
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user01', 2, 5, 'great book');

INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user02', 1, 15.00, '2018-03-03 09:01:52');
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user03', 1, 16.00, '2018-03-03 09:02:52');
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user02', 1, 17.00, '2018-03-03 09:03:52');
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user03', 1, 18.00, '2018-03-03 09:04:52');
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user02', 1, 20.00, '2018-03-03 09:05:52');
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user02', 2, 19.00, '2018-03-03 09:06:52');
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user02', 3, 18.00, '2018-03-03 09:07:52');
INSERT INTO Bid(username, item_id, bid_amount, bid_time) VALUES ('user03', 3, 21.00, '2018-03-03 09:08:52');





  
