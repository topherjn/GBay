-- **********************************
-- DDL for GT_Bay DB
-- CREATE DATABASE GT_BAY;
USE GT_BAY;

-- Start fresh delete existing tables
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS GTBayUser;
DROP TABLE IF EXISTS RegularUser;
DROP TABLE IF EXISTS AdminUser;
DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS Rating;
DROP TABLE IF EXISTS Bid;

-- Create the tables
CREATE TABLE Category (
   category_id INT NOT NULL,
   description TEXT,
   PRIMARY KEY (category_id)
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
	 position VARCHAR(50) NULL,
   FOREIGN KEY (username) REFERENCES RegularUser(username),
   PRIMARY KEY (username)
);

CREATE TABLE Item(
   item_id INT NOT NULL AUTO_INCREMENT,
   item_name VARCHAR(50) NOT NULL,
   description TEXT NOT NULL,
   item_condition INT NOT NULL,
   returnable BOOLEAN NOT NULL DEFAULT false,
   starting_bid DECIMAL(10,2) NOT NULL,
   minimum_sale DECIMAL(10,2) NOT NULL,
   auction_length INT NOT NULL,
   get_it_now DECIMAL(10,2) NULL,
   start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
   category_id INT NOT NULL, -- FKey
   listing_username VARCHAR(50) NOT NULL, -- FKey
   FOREIGN KEY (category_id) REFERENCES Category(category_id),
   FOREIGN KEY (listing_username) REFERENCES RegularUser(username),
   PRIMARY KEY (item_id)
);



CREATE TABLE Rating(
   username VARCHAR(50) NOT NULL,
   item_id INT NOT NULL,
   numstars INT NOT NULL,
   comments TEXT NOT NULL,
   date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
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


-- **********************************
-- Insert category data
INSERT INTO Category(category_id, description) VALUES (1, 'Art');
INSERT INTO Category(category_id, description) VALUES (2, 'Books');
INSERT INTO Category(category_id, description) VALUES (3, 'Electronics');
INSERT INTO Category(category_id, description) VALUES (4, 'Home and Garden');
INSERT INTO Category(category_id, description) VALUES (5, 'Sports Goods');
INSERT INTO Category(category_id, description) VALUES (6, 'Toys');
INSERT INTO Category(category_id, description) VALUES (7, 'Other');

-- Add an admin user
INSERT INTO RegularUser(username, password, first_name, last_name) VALUES ('admin01', 'password', 'Pierre', 'Omidyar');
INSERT INTO AdminUser(username, position) VALUES ('admin01', 'DBA');

-- Add regular User
INSERT INTO RegularUser(username, password, first_name, last_name) VALUES ('user01', 'password', 'Dan', 'Smith');
INSERT INTO RegularUser(username, password, first_name, last_name) VALUES ('user02', 'password', 'Amy', 'Smith');
INSERT INTO RegularUser(username, password, first_name, last_name) VALUES ('user03', 'password', 'Anne', 'Smith');


INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, minimum_sale, get_it_now, auction_length, category_id, listing_username)
   VALUES ('clock radio', 'digital clock radio', 1, false, 15.00, 20.00, 30.00, 5, 3, 'user02');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, minimum_sale, get_it_now, auction_length, category_id, listing_username)
   VALUES ('moby dick', 'classic book', 1, false, 10.00, 15.00, 20.00, 3, 2, 'user03');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, minimum_sale, get_it_now, auction_length, category_id, listing_username)
   VALUES ('ipod classic', 'like new ipod', 2, false, 15.00, 20.00, 30.00, 5, 3, 'user02');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, minimum_sale, get_it_now, auction_length, category_id, listing_username)
   VALUES ('fishing boat', '12 foot fishing boat', 1, false, 150.00, 200.00, 300.00, 5, 5, 'user03');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, minimum_sale, get_it_now, auction_length, category_id, listing_username)
   VALUES ('clock radio', 'digital clock radio', 1, false, 16.00, 21.00, 31.00, 5, 3, 'user03');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, minimum_sale, get_it_now, auction_length, category_id, listing_username)
   VALUES ('surfboard', 'retro board', 1, false, 160.00, 210.00, NULL, 5, 3, 'user03');


INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user02', 1, 5, 'great product');
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user03', 1, 3, 'its ok alarm to quiet');
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user03', 2, 3, 'to long');
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user01', 2, 5, 'great book');

INSERT INTO Bid(username, item_id, bid_amount) VALUES ('user02', 1, 30.00);
INSERT INTO Bid(username, item_id, bid_amount) VALUES ('user02', 2, 19.00);
INSERT INTO Bid(username, item_id, bid_amount) VALUES ('user02', 3, 18.00);
INSERT INTO Bid(username, item_id, bid_amount) VALUES ('user03', 3, 21.00);





  
