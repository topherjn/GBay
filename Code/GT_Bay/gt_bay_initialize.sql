-- **********************************
-- DDL for GT_Bay DB
USE GT_BAY;

-- Start fresh delete existing tables
DROP TABLE IF EXISTS CATEGORY;
DROP TABLE IF EXISTS ITEM_CONDITION;

DROP TABLE IF EXISTS GT_BAY_USER;
DROP TABLE IF EXISTS ITEM;
DROP TABLE IF EXISTS RATING;
DROP TABLE IF EXISTS BID;
DROP TABLE IF EXISTS AUCTION;

-- Create the tables
CREATE TABLE CATEGORY (
   category_id INT NOT NULL,
   description TEXT,
   PRIMARY KEY (category_id)
);

CREATE TABLE ITEM_CONDITION (
   condition_id INT NOT NULL,
   description  VARCHAR(50),
   PRIMARY KEY (condition_id)
);

CREATE TABLE GT_BAY_USER(
 	user_id INT NOT NULL AUTO_INCREMENT,
	username VARCHAR(50) NOT NULL UNIQUE,
	password VARCHAR(50) NOT NULL,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	is_admin BOOLEAN NOT NULL,
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
   PRIMARY KEY (item_id)
);
 

CREATE TABLE RATING(
	user_id INT NOT NULL,
	item_id INT NOT NULL,
	numstars INT NOT NULL,
	comment VARCHAR(50) NOT NULL,
   PRIMARY KEY (user_id,item_id)
); 

CREATE TABLE BID(
	user_id INT NOT NULL,
	auction_id INT NOT NULL,
	bid_amount DECIMAL(10,2) NOT NULL,
	bid_time TIMESTAMP NOT NULL,
 PRIMARY KEY (user_id,auction_id)
); 

CREATE TABLE AUCTION(
	auction_id INT NOT NULL,
	item_id INT NOT NULL,
	starting_bid DECIMAL(10,2) NOT NULL,
	minimum_sale DECIMAL(10,2) NOT NULL,
	auction_length INT NOT NULL,
	get_it_now DECIMAL(10,2) NULL,
	posted_by INT NOT NULL,
	winner INT NULL,
	start_time TIMESTAMP NOT NULL,
 PRIMARY KEY (auction_id)
); 

-- **********************************
-- Insert some data
-- insert into CATEGORY(category_id, description) values (1, 'Art')
-- insert into CATEGORY(category_id, description) values (2, 'Books')
-- insert into CATEGORY(category_id, description) values (3, 'Electronics')
-- insert into CATEGORY(category_id, description) values (4, 'Home and Garden')
-- insert into CATEGORY(category_id, description) values (5, 'Sports Goods')
-- insert into CATEGORY(category_id, description) values (6, 'Toys')
-- insert into CATEGORY(category_id, description) values (7, 'Other')

-- insert into GT_BAY_USER(username, password, first_name, last_name, is_admin, position) values ()
 
