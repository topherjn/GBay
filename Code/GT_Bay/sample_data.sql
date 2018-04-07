-- **********************************
-- DDL for cs6400_spr18_team047 DB
-- Sample data

CREATE DATABASE cs6400_spr18_team047_sample_data;
USE cs6400_spr18_team047_sample_data;


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

CREATE VIEW CategoryReport AS
SELECT	  c.category_name     AS 'Category',
                count(get_it_now_price) AS 'Total Items',
                min(i.get_it_now_price) AS 'Min Price',
                max(get_it_now_price)   AS 'Max Price',
                ROUND(avg(get_it_now_price),2)   AS 'Average Price'
            FROM Category c LEFT OUTER JOIN Item i ON c.category_id = i.category_id
            GROUP BY c.category_id
            ORDER BY c.category_name;

CREATE VIEW UniqueRatings AS
SELECT r.username, i.item_name
FROM Rating r INNER JOIN Item i ON r.item_id = i.item_id;


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
INSERT INTO RegularUser(username, password, first_name, last_name) VALUES ('admin1', 'opensesame', 'Riley', 'Fuiss');
INSERT INTO RegularUser(username, password, first_name, last_name) VALUES ('admin2', 'opensesayou', 'Tonnis', 'Kinser');

-- Add an admin user
INSERT INTO AdminUser(username, position) VALUES ('admin1', 'Technical Support');
INSERT INTO AdminUser(username, position) VALUES ('admin2', 'Chief Techy');



INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
   VALUES ('Garmin GPS', 'This is a great GPS', 3, false, 50.00, 70.00, 99.00,'2018-03-31 12:22', 3, 'user1');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
   VALUES ('Canon Powershot', 'Point and shoot!', 2, false, 40.00, 60.00, 80.00,'2018-04-01 14:14:00', 3, 'user1');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
   VALUES ('Nikon D3', 'New and in box!', 4, false, 1500.00, 1800.00, 2000.00,'2018-04-05 09:19:00', 3, 'user2');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
   VALUES ('Danish Art Book', 'Delicious Danish Art', 3, true, 10.00, 10.00, 10.00,'2018-04-05 15:33:00', 1, 'user3');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
   VALUES ('SQL in 10 Minutes', 'Learn SQL really fast!', 1, false, 5.00, 10.00, 10.00,'2018-04-05 16:48:00', 2, 'admin1');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
   VALUES ('SQL in 8 Minutes', 'Learn SQL even fastter!', 2, false, 5.00, 8.00, 8.00,'2018-04-08 10:01:00', 2, 'admin2');
INSERT INTO Item(item_name, description, item_condition, returnable, starting_bid, min_sale_price, get_it_now_price, auction_end_time, category_id, listing_username)
   VALUES ('Pull-up Bar', 'Works on any door frame', 4, false, 20.00, 25.00, 40.00,'2018-04-09 22:09:00', 5, 'user6');


INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user2', 1, 5, 'Great GPS!');
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user3', 1, 2, 'Not so great GPS!');
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user4', 1, 4, 'A favorite of mine.');
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user1', 4, 1, 'Go for the italian stuff instead.');
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('admin1', 6, 1, 'Not recommended.');
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user1', 6, 3, 'This book is okay.');
INSERT INTO Rating(username, item_id, numstars, comments) VALUES ('user2', 6, 5, 'I learned SQL in 8 minutes!');



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



