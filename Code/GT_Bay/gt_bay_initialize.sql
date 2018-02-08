-- **********************************
-- DDL for GT_Bay DB
-- CREATE DATABASE GT_BAY;
USE GT_BAY;

-- Start fresh delete existing tables
DROP TABLE IF EXISTS CATEGORY;
DROP TABLE IF EXISTS GT_BAY_USER;
DROP TABLE IF EXISTS ITEM;
DROP TABLE IF EXISTS RATING;
DROP TABLE IF EXISTS BID;

-- Create the tables
CREATE TABLE CATEGORY (
   category_id INT NOT NULL,
   description TEXT,
   PRIMARY KEY (category_id)
);

CREATE TABLE GT_BAY_USER(
 	 user_id INT NOT NULL AUTO_INCREMENT,
	 username VARCHAR(50) NOT NULL UNIQUE,
	 password VARCHAR(50) NOT NULL,
	 first_name VARCHAR(50) NOT NULL,
	 last_name VARCHAR(50) NOT NULL,
	 is_admin BOOLEAN NOT NULL DEFAULT false,
	 position VARCHAR(50) NULL,
   PRIMARY KEY (user_id)
);

CREATE TABLE ITEM(
   item_id INT NOT NULL AUTO_INCREMENT,
   item_name VARCHAR(50) NOT NULL,
   description VARCHAR(50) NOT NULL,
   item_condition INT NOT NULL,
   returnable BOOLEAN NOT NULL DEFAULT false,
   starting_bid DECIMAL(10,2) NOT NULL,
   minimum_sale DECIMAL(10,2) NOT NULL,
   auction_length INT NOT NULL,
   get_it_now DECIMAL(10,2) NULL,
   winner INT NULL,
   start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
   category_id INT NOT NULL, -- FKey
   listing_user_id INT NOT NULL, -- FKey
   winner_user_id INT NULL, -- FKey
   PRIMARY KEY (item_id)
);

CREATE TABLE RATING(
   user_id INT NOT NULL,
   item_id INT NOT NULL,
   numstars INT NOT NULL,
   comments VARCHAR(50) NOT NULL,
   date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   PRIMARY KEY (user_id,item_id)
); 

CREATE TABLE BID(
   user_id INT NOT NULL,
   item_id INT NOT NULL,
   bid_amount DECIMAL(10,2) NOT NULL,
   bid_time TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (user_id, item_id)
); 

-- **********************************
-- Insert category data
INSERT INTO CATEGORY(category_id, description) VALUES (1, 'Art');
INSERT INTO CATEGORY(category_id, description) VALUES (2, 'Books');
INSERT INTO CATEGORY(category_id, description) VALUES (3, 'Electronics');
INSERT INTO CATEGORY(category_id, description) VALUES (4, 'Home and Garden');
INSERT INTO CATEGORY(category_id, description) VALUES (5, 'Sports Goods');
INSERT INTO CATEGORY(category_id, description) VALUES (6, 'Toys');
INSERT INTO CATEGORY(category_id, description) VALUES (7, 'Other');

-- Add an admin user
INSERT INTO GT_BAY_USER(username, password, first_name, last_name, is_admin, position) VALUES ('admin', 'password', 'Pierre', 'Omidyar', True, 'DBA');

-- Add regular User
INSERT INTO GT_BAY_USER(username, password, first_name, last_name) VALUES ('user01', 'password', 'Dan', 'Smith');
INSERT INTO GT_BAY_USER(username, password, first_name, last_name) VALUES ('user02', 'password', 'Amy', 'Smith');
INSERT INTO GT_BAY_USER(username, password, first_name, last_name) VALUES ('user03', 'password', 'Anne', 'Smith');

INSERT INTO ITEM(item_name, description, item_condition, returnable, starting_bid, minimum_sale, get_it_now, auction_length, category_id, listing_user_id) 
   VALUES ('clock radio', 'digital clock radio', 1, false, 15.00, 20.00, 30.00, 5, 3, 2);
INSERT INTO ITEM(item_name, description, item_condition, returnable, starting_bid, minimum_sale, get_it_now, auction_length, category_id, listing_user_id) 
   VALUES ('moby dick', 'classic book', 1, false, 10.00, 15.00, 20.00, 3, 2, 3);
INSERT INTO ITEM(item_name, description, item_condition, returnable, starting_bid, minimum_sale, get_it_now, auction_length, category_id, listing_user_id) 
   VALUES ('ipod classic', 'like new ipod', 2, false, 15.00, 20.00, 30.00, 5, 3, 2);
INSERT INTO ITEM(item_name, description, item_condition, returnable, starting_bid, minimum_sale, get_it_now, auction_length, category_id, listing_user_id) 
   VALUES ('fishing boat', '12 foot fishing boat', 1, false, 150.00, 200.00, 300.00, 5, 5, 3);
INSERT INTO ITEM(item_name, description, item_condition, returnable, starting_bid, minimum_sale, get_it_now, auction_length, category_id, listing_user_id) 
   VALUES ('clock radio', 'digital clock radio', 1, false, 16.00, 21.00, 31.00, 5, 3, 3);


INSERT INTO RATING(user_id, item_id, numstars, comments) VALUES (2, 1, 5, 'great product');
INSERT INTO RATING(user_id, item_id, numstars, comments) VALUES (3, 1, 3, 'its ok alarm to quiet');
INSERT INTO RATING(user_id, item_id, numstars, comments) VALUES (3, 2, 3, 'to long');
INSERT INTO RATING(user_id, item_id, numstars, comments) VALUES (4, 2, 5, 'great book');

INSERT INTO BID(user_id, item_id, bid_amount) VALUES (2, 1, 30.00);
INSERT INTO BID(user_id, item_id, bid_amount) VALUES (2, 2, 19.00);
INSERT INTO BID(user_id, item_id, bid_amount) VALUES (2, 3, 18.00);
INSERT INTO BID(user_id, item_id, bid_amount) VALUES (3, 3, 21.00);





  
