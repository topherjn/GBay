-- SQL For Team 047 Phase 2 Report

-- ---------------------------------------------------------------------------------------
-- Login

-- Test data
SET @$username='user04', @$password='password', @$firstName='Larry', @$lastName='Ellison';
SET @$username='admin01', @$password='password';

-- Select Login User of any type
SELECT
  RegularUser.password,
  AdminUser.position
FROM RegularUser
  LEFT JOIN AdminUser ON RegularUser.username = AdminUser.username
WHERE RegularUser.username = @$username;


-- ---------------------------------------------------------------------------------------
-- Register

-- Test data
SET @$username='user05', @$password='password', @$firstName='Larry', @$lastName='Ellison';

-- Insert Regular User
INSERT INTO RegularUser (username, password,
                         first_name, last_name)
VALUES (@$username, @$password,
        @$firstName, @$lastName);


-- ---------------------------------------------------------------------------------------
-- Add Item

-- Test data
SET @$itemName='GT T-Shirt', @$description='100 Percent cotton T', @$itemCondition=5, @$returnable=false;
SET @$startingBid='10.00', @$minimumSale=15.00, @$getItNow=20.00, @$auctionLength=5;
SET @$categoryId=3, @$listingUsername='user01';

-- Populate Category Dropdown
SELECT category_id, category_name FROM CATEGORY ORDER BY category_id;


-- Persist Values
INSERT INTO Item (item_name, description, item_condition, returnable,
                  starting_bid, min_sale_price, get_it_now_price, auction_length,
                  auction_end_time, category_id, listing_username)
VALUES (@$itemName, @$description, @$itemCondition, @$returnable,
                    @$startingBid, @$minimumSale, @$getItNow, @$auctionLength,
                    DATE_ADD(NOW(), INTERVAL @$auctionLength DAY), @$categoryId, @$listingUsername);

-- ---------------------------------------------------------------------------------------
-- Item Search

-- Test data
SET @$keyword='clock', @$categoryName=NULL, @$minPrice=NULL, @$maxPrice=NULL, @$conditionAtLeast=NULL;
SET @$keyword='GT T-Shirt', @$categoryName='Electronics', @$minPrice=6.00, @$maxPrice=9.00, @$conditionAtLeast=NULL;

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
      AND (item_name LIKE CONCAT('%', @$keyword, '%')
           OR description LIKE CONCAT('%', @$keyword, '%'))
      AND (@$category IS NULL
           OR category_name = @$category)
      AND (@$minPrice IS NULL OR
           IF(bid_amount IS NULL, starting_bid, bid_amount)
           >= @$minPrice)
      AND (@$maxPrice IS NULL OR
           IF(bid_amount IS NULL, starting_bid, bid_amount)
           <= @$maxPrice)
      AND (@$conditionAtLeast IS NULL OR
           item_condition >= @$conditionAtLeast)
ORDER BY auction_end_time;


-- Execute Search
SELECT
  Item.item_id,
  item_name,
  bid_amount AS current_bid,
  username   AS high_bidder,
  get_it_now_price,
  auction_end_time,
  IF(CurrentBid.bid_amount IS NULL, starting_bid, CurrentBid.bid_amount) AS price,
  category_name
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
      AND (item_name LIKE CONCAT('%', @$keyword, '%')
           OR description LIKE CONCAT('%', @$keyword, '%'))
      AND (@$categoryName IS NULL
           OR category_name = @$categoryName)
      AND (@$minPrice IS NULL OR
           (IF(CurrentBid.bid_amount IS NULL, starting_bid, CurrentBid.bid_amount))
           >= @$minPrice)
      AND (@$maxPrice IS NULL OR
           IF(CurrentBid.bid_amount IS NULL, starting_bid, CurrentBid.bid_amount)
           <= @$maxPrice)
      AND (@$conditionAtLeast IS NULL OR
           item_condition >= @$conditionAtLeast)
ORDER BY auction_end_time;



-- ---------------------------------------------------------------------------------------
-- View Sale Item

-- Test data
SET @$itemId=1;

-- View Item details
SELECT
  i.item_name,
  i.description,
  c.category_name,
  i.item_condition,
  i.get_it_now_price,
  i.returnable,
  i.auction_end_time
FROM Item i INNER JOIN Category c ON i.category_id = c.category_id
WHERE i.item_id = @$itemId;

-- View Top Bids
SELECT
  b.bid_amount AS 'Bid Amount',
  b.bid_time   AS 'Time of Bid',
  u.username   AS 'Username'
FROM Bid b INNER JOIN RegularUser u ON b.username = u.username
WHERE b.item_id = @$itemId
ORDER BY b.bid_amount DESC
LIMIT 4;

-- Display New Bid Input Field
SELECT
    IF(IFNULL(max(b.bid_amount),0) >= i.starting_bid,
        max(b.bid_amount)+1,
       i.starting_bid) as 'min_bid'

FROM Item i JOIN Bid b ON b.item_id = i.item_id
WHERE i.item_id = @$itemId;


-- ---------------------------------------------------------------------------------------
-- Bid on Item

-- Test data
SET @$username='user01', @$itemId=3, @$bidAmount=23.00;

-- Insert bid
INSERT INTO Bid (username, item_id, bid_amount)
VALUES (@$username, @$itemId, @$bidAmount);


-- ---------------------------------------------------------------------------------------
-- Get It Now

-- Test data
SET @$username='user01', @$itemId=3, @$currentTime='2018-03-01 14:01:52';

UPDATE Item
SET auction_end_time =
IF(auction_end_time > @$currentTime,
   @$currentTime, auction_end_time)
WHERE item_id = @$itemId;

INSERT INTO Bid
(username, item_id, bid_amount, bid_time)
  SELECT
    @$username,
    item_id,
    get_it_now_price,
    @$currentTime
  FROM Item
  WHERE Item.item_id = @$itemID AND
        Item.auction_end_time = @$currentTime;


-- ---------------------------------------------------------------------------------------
-- Update Description

-- Test data
SET @$itemId=3, @$description='very nice condition ipod classic';

-- update description
UPDATE Item
SET description = @$description
WHERE item_id = @$itemId;


-- ---------------------------------------------------------------------------------------
-- View Item Ratings

-- Test data
SET @$itemId=3;

-- select item name
SELECT item_name
FROM Item
WHERE item_id = @$itemId;

-- select average number of stars
SELECT AVG(numstars)
FROM Rating
WHERE item_id = @$itemId;

-- rating details
SELECT username as ratingUsername, numstars, rating_time, comments
FROM Rating
WHERE item_id = @$itemId
ORDER BY rating_time DESC;


-- ---------------------------------------------------------------------------------------
-- Add / Delete Item Ratings

-- Test data
SET @$itemId=2, @$username='user02', @$nbrStars=4, @$comments='worth buying again';

-- Insert Rating
INSERT INTO Rating (username, item_id, numstars, comments)
VALUES (@$username, @$itemId, @$nbrStars, @$comments);

-- Delete Rating
DELETE FROM Rating
WHERE username = @$username AND item_id = @$itemId;


-- ---------------------------------------------------------------------------------------
-- Compute Winner / View Auction Results

SELECT
  i.item_id,
  i.item_name,
  IF(b.max_bid >= i.min_sale_price, b.max_bid, NULL)
    AS max_bid,
  IF(b.max_bid >= i.min_sale_price, b.username, NULL)
    AS username,
  i.auction_end_time
FROM Item i
  LEFT JOIN (
              -- SELECT the highest bid amounts FOR ALL auctions
               SELECT item_id, bid_amount AS max_bid, username
                      FROM Bid b1 NATURAL JOIN
            (SELECT item_id, max(bid_amount) AS bid_amount
                                             FROM Bid GROUP BY item_id) AS b2
            ) b ON b.item_id = i.item_id
WHERE i.auction_end_time < NOW();

/*SELECT
  i.item_id,
  i.item_name,
  b.max_bid,
  b.username,
  i.auction_end_time
FROM Item i
  LEFT JOIN (
              -- Select the highest bid amounts for all ended auctions
              SELECT
                b.item_id,
                b.username,
                max(b.bid_amount) AS 'max_bid',
                b.bid_time
              FROM Bid b
              WHERE b.bid_time < NOW()
              GROUP BY b.item_id
            ) b ON b.item_id = i.item_id
WHERE i.auction_end_time < NOW() AND (b.max_bid IS NULL OR b.max_bid >= i.min_sale_price);
*/


-- ---------------------------------------------------------------------------------------
-- View Category Report

SELECT
  c.category_name     AS 'Category',
  count(get_it_now_price) AS 'Total Items',
  min(i.get_it_now_price) AS 'Min Price',
  max(get_it_now_price)   AS 'Max Price',
  avg(get_it_now_price)   AS 'Average Price'
FROM category c LEFT OUTER JOIN item i ON c.category_id = i.category_id
GROUP BY c.category_id
ORDER BY c.category_name;


-- ---------------------------------------------------------------------------------------
-- View User Report

-- listed items
SELECT
  listing_username,
  COUNT(listing_username)
FROM item
GROUP BY listing_username;


-- Sold Items
SELECT
  listing_username,
  COUNT(*)
FROM Bid b1
  NATURAL JOIN
  (SELECT
     item_id,
     max(bid_amount) AS bid_amount
   FROM Bid
   GROUP BY item_id) AS b2
  NATURAL JOIN Item i
WHERE auction_end_time < NOW()
      AND bid_amount >= min_sale_price
GROUP BY listing_username;

/*SELECT
  b.username,
  count(i.item_id)
FROM Item i
  LEFT JOIN (
              -- Select the highest bid amounts for all ended auctions
              SELECT
                b.item_id,
                b.username,
                max(b.bid_amount) AS 'max_bid',
                b.bid_time
              FROM Bid b
              WHERE b.bid_time < NOW()
              GROUP BY b.item_id
            ) b ON b.item_id = i.item_id
WHERE i.auction_end_time < NOW() AND (b.max_bid >= i.minimum_sale)
GROUP BY b.username;*/

-- Purchased
SELECT
  username,
  COUNT(*)
FROM Bid b1
  NATURAL JOIN
  (SELECT
     item_id,
     max(bid_amount) AS bid_amount
   FROM Bid
   GROUP BY item_id) AS b2
  NATURAL JOIN Item i
WHERE auction_end_time < NOW()
      AND bid_amount >= min_sale_price
GROUP BY username;


SELECT username, COUNT(username)
FROM rating
GROUP BY username;


-- ------------------------------------------------------------------
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
                  AND (item_name LIKE CONCAT('%', 'ipod', '%')
                       OR description LIKE CONCAT('%', 'ipod', '%'))
                  AND (0 IS NULL
                       OR category_name = 0)
                  AND (NULL IS NULL OR
                       IF(bid_amount IS NULL, starting_bid, bid_amount)
                       >= NULL)
                  AND ( NULL IS NULL OR
                       IF(bid_amount IS NULL, starting_bid, bid_amount)
                       <= NULL )
                  AND (0 IS NULL OR
                       item_condition >= 0)
            ORDER BY auction_end_time;


INSERT INTO Bid (username, item_id, bid_amount)
        SELECT 'user02', 9, 10.00
        WHERE (SELECT auction_end_time from Item where item_id = 9) > CURRENT_TIMESTAMP
          AND ((SELECT count(*) from Bid where item_id = 9) = 0
               OR (SELECT max(bid_amount) + 1 from Bid where item_id = 9) <= 10.00);
