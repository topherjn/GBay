-- **********************************
-- DDL for GT_Bay DB
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
   category INT NOT NULL,
   returnable BOOLEAN NOT NULL,
   starting_bid DECIMAL(10,2) NOT NULL,
   minimum_sale DECIMAL(10,2) NOT NULL,
   auction_length INT NOT NULL,
   get_it_now DECIMAL(10,2) NULL,
   posted_by INT NOT NULL,
   winner INT NULL,
   start_time TIMESTAMP NOT NULL,
   PRIMARY KEY (item_id)
);

CREATE TABLE RATING(
   user_id INT NOT NULL,
   item_id INT NOT NULL,
   numstars INT NOT NULL,
   comment VARCHAR(50) NOT NULL,
   date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   PRIMARY KEY (user_id,item_id)
); 

CREATE TABLE BID(
   user_id INT NOT NULL,
   auction_id INT NOT NULL,
   bid_amount DECIMAL(10,2) NOT NULL,
   bid_time TIMESTAMP NOT NULL,
   PRIMARY KEY (user_id,auction_id)
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
INSERT INTO GT_BAY_USER(username, password, first_name, last_name, is_admin, position) VALUES ('admin', 'password', 'Pierre', 'Omidyar', True, 'DBA')

