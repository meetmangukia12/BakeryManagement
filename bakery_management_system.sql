-- ============================================================
--  BAKERY MANAGEMENT SYSTEM
--  Database Management Class Project
--  Description: A MySQL-based bakery management system that
--               tracks customers, custom cake configurations,
--               and orders to improve bakery workflow.
-- ============================================================


-- ============================================================
--  SECTION 1: DATABASE & TABLE CREATION
-- ============================================================

CREATE DATABASE IF NOT EXISTS BakeryManagementDB;
USE BakeryManagementDB;

-- ----------------------------
-- Table 1: Customer
-- Stores all customer information
-- ----------------------------
CREATE TABLE IF NOT EXISTS Customer (
    Customer_id     INT             AUTO_INCREMENT PRIMARY KEY,
    Customer_name   VARCHAR(100)    NOT NULL,
    Customer_age    INT             CHECK (Customer_age >= 0),
    Customer_email  VARCHAR(150),
    Customer_phone  VARCHAR(20)
);

-- ----------------------------
-- Table 2: Cake
-- Stores all cake configurations
-- Each cake is linked to a Customer who designed it
-- ----------------------------
CREATE TABLE IF NOT EXISTS Cake (
    Cake_id         INT             AUTO_INCREMENT PRIMARY KEY,
    Customer_id     INT             NOT NULL,
    Cake_shape      VARCHAR(50)     NOT NULL,       -- e.g., Round, Square, Heart
    Cake_batter     VARCHAR(50)     NOT NULL,       -- e.g., Vanilla, Chocolate, Red Velvet
    Side_frosting   VARCHAR(50)     NOT NULL,       -- e.g., Buttercream, Fondant
    Top_frosting    VARCHAR(50)     NOT NULL,       -- e.g., Ganache, Whipped Cream
    Decoration_1    VARCHAR(100)    NOT NULL,       -- e.g., Fresh Flowers, Sprinkles
    Decoration_2    VARCHAR(100),                  -- Optional second decoration
    Layers          INT             NOT NULL        -- 1 to 5 layers
                    CHECK (Layers BETWEEN 1 AND 5),
    FOREIGN KEY (Customer_id) REFERENCES Customer(Customer_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ----------------------------
-- Table 3: Order
-- Stores finalized order details
-- Each order is linked to a specific Cake
-- ----------------------------
CREATE TABLE IF NOT EXISTS `Order` (
    Order_id          INT             AUTO_INCREMENT PRIMARY KEY,
    Cake_id           INT             NOT NULL,
    Order_occasion    VARCHAR(100),               -- e.g., Birthday, Wedding, Anniversary
    Shipping_address  VARCHAR(255)    NOT NULL,
    Order_price       DECIMAL(10, 2)  NOT NULL,
    Order_date        DATE            NOT NULL,
    FOREIGN KEY (Cake_id) REFERENCES Cake(Cake_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- ============================================================
--  SECTION 2: INSERT SAMPLE DATA
-- ============================================================

-- Insert Customers
INSERT INTO Customer (Customer_name, Customer_age, Customer_email, Customer_phone)
VALUES
    ('Alice Johnson',   30, 'alice@email.com',   '201-555-0101'),
    ('Bob Martinez',    45, 'bob@email.com',     '201-555-0202'),
    ('Carol White',     28, 'carol@email.com',   '201-555-0303'),
    ('David Kim',       52, 'david@email.com',   '201-555-0404'),
    ('Emma Thompson',   35, 'emma@email.com',    '201-555-0505'),
    ('Frank Nguyen',    22, 'frank@email.com',   '201-555-0606');

-- Insert Cakes
INSERT INTO Cake (Customer_id, Cake_shape, Cake_batter, Side_frosting, Top_frosting, Decoration_1, Decoration_2, Layers)
VALUES
    (1, 'Round',    'Vanilla',      'Buttercream',  'Whipped Cream',    'Fresh Flowers',    'Gold Leaf',        2),
    (2, 'Square',   'Chocolate',    'Fondant',      'Ganache',          'Sprinkles',        NULL,               3),
    (3, 'Heart',    'Red Velvet',   'Buttercream',  'Cream Cheese',     'Edible Glitter',   'Fresh Berries',    1),
    (4, 'Round',    'Lemon',        'Swiss Meringue','Lemon Curd',      'Candied Lemon',    NULL,               4),
    (5, 'Square',   'Carrot',       'Cream Cheese', 'Whipped Cream',    'Walnut Crumble',   'Cinnamon Drizzle', 2),
    (6, 'Round',    'Funfetti',     'Buttercream',  'Whipped Cream',    'Rainbow Sprinkles','Edible Stars',     3);

-- Insert Orders
INSERT INTO `Order` (Cake_id, Order_occasion, Shipping_address, Order_price, Order_date)
VALUES
    (1, 'Birthday',     '12 Oak Street, Ridgewood, NJ 07450',       85.00,  '2025-04-05'),
    (2, 'Wedding',      '88 Maple Ave, Paramus, NJ 07652',          150.00, '2025-04-08'),
    (3, 'Anniversary',  '301 Pine Road, Hackensack, NJ 07601',      72.50,  '2025-04-10'),
    (4, 'Birthday',     '55 Elm Drive, Fair Lawn, NJ 07410',        120.00, '2025-04-12'),
    (5, 'Graduation',   '19 Birch Lane, Wyckoff, NJ 07481',         95.00,  '2025-04-15'),
    (6, 'Birthday',     '7 Willow Court, Glen Rock, NJ 07452',      110.00, '2025-04-18');


-- ============================================================
--  SECTION 3: SQL STATEMENTS (WORKFLOW DEMONSTRATION)
-- ============================================================

-- ----------------------------
-- SQL Statement 1: SEARCH — Browse all available cake configurations
-- Use case: A baker wants to review every custom cake on file
-- ----------------------------
SELECT
    c.Cake_id,
    cu.Customer_name,
    c.Cake_shape,
    c.Cake_batter,
    c.Side_frosting,
    c.Top_frosting,
    c.Decoration_1,
    COALESCE(c.Decoration_2, 'None') AS Decoration_2,
    c.Layers
FROM Cake c
JOIN Customer cu ON c.Customer_id = cu.Customer_id
ORDER BY c.Cake_id;

-- ----------------------------
-- SQL Statement 2: PLACE AN ORDER — Insert a new order for a customer
-- Use case: Customer Alice (id=1) places an order for her cake (id=1)
-- ----------------------------
INSERT INTO `Order` (Cake_id, Order_occasion, Shipping_address, Order_price, Order_date)
VALUES (1, 'Baby Shower', '12 Oak Street, Ridgewood, NJ 07450', 95.00, '2025-05-01');

-- ----------------------------
-- SQL Statement 3: SEARCH ORDERS BY OCCASION — Find all Birthday orders
-- Use case: Baker reviews upcoming birthday cakes to prepare
-- ----------------------------
SELECT
    o.Order_id,
    cu.Customer_name,
    o.Order_occasion,
    o.Order_date,
    o.Order_price,
    o.Shipping_address
FROM `Order` o
JOIN Cake c    ON o.Cake_id = c.Cake_id
JOIN Customer cu ON c.Customer_id = cu.Customer_id
WHERE o.Order_occasion = 'Birthday'
ORDER BY o.Order_date;

-- ----------------------------
-- SQL Statement 4: UPDATE — Modify a cake's frosting before baking
-- Use case: Customer requests a last-minute change to Side_frosting
-- ----------------------------
UPDATE Cake
SET Side_frosting = 'Swiss Meringue'
WHERE Cake_id = 1;

-- ----------------------------
-- SQL Statement 5: GENERATE INVOICE — Retrieve full order details for billing
-- Use case: Generate an invoice for Order #2
-- ----------------------------
SELECT
    o.Order_id                          AS Invoice_Number,
    cu.Customer_name,
    cu.Customer_email,
    cu.Customer_phone,
    o.Order_occasion,
    o.Order_date,
    c.Cake_shape,
    c.Cake_batter,
    c.Layers,
    c.Side_frosting,
    c.Top_frosting,
    c.Decoration_1,
    COALESCE(c.Decoration_2, 'N/A')    AS Decoration_2,
    o.Shipping_address,
    o.Order_price                       AS Total_Due
FROM `Order` o
JOIN Cake c         ON o.Cake_id = c.Cake_id
JOIN Customer cu    ON c.Customer_id = cu.Customer_id
WHERE o.Order_id = 2;

-- ----------------------------
-- SQL Statement 6: REVENUE REPORT — Calculate total revenue by occasion type
-- Use case: Manager analyzes which occasions drive the most sales
-- ----------------------------
SELECT
    Order_occasion,
    COUNT(*)                    AS Total_Orders,
    SUM(Order_price)            AS Total_Revenue,
    ROUND(AVG(Order_price), 2)  AS Average_Price
FROM `Order`
GROUP BY Order_occasion
ORDER BY Total_Revenue DESC;

-- ----------------------------
-- SQL Statement 7: DELETE — Remove a cancelled order
-- Use case: A customer cancels their order before it is baked
-- ----------------------------
DELETE FROM `Order`
WHERE Order_id = 7;   -- This removes the Baby Shower order inserted in Statement 2

-- ----------------------------
-- SQL Statement 8: SEARCH ORDERS BY DATE RANGE — Upcoming orders this week
-- Use case: Baker prepares the production schedule for the week
-- ----------------------------
SELECT
    o.Order_id,
    cu.Customer_name,
    o.Order_occasion,
    c.Cake_batter,
    c.Layers,
    o.Order_date,
    o.Shipping_address
FROM `Order` o
JOIN Cake c     ON o.Cake_id = c.Cake_id
JOIN Customer cu ON c.Customer_id = cu.Customer_id
WHERE o.Order_date BETWEEN '2025-04-10' AND '2025-04-18'
ORDER BY o.Order_date;


-- ============================================================
--  SECTION 4: VIEWS
-- ============================================================

-- ----------------------------
-- View 1: vw_Order_Details
-- Purpose: A full summary of every order, combining customer,
--          cake, and order information in one convenient view.
--          Used by staff to look up any order at a glance.
-- ----------------------------
CREATE OR REPLACE VIEW vw_Order_Details AS
SELECT
    o.Order_id,
    cu.Customer_id,
    cu.Customer_name,
    cu.Customer_email,
    cu.Customer_phone,
    c.Cake_shape,
    c.Cake_batter,
    c.Layers,
    c.Side_frosting,
    c.Top_frosting,
    c.Decoration_1,
    COALESCE(c.Decoration_2, 'None') AS Decoration_2,
    o.Order_occasion,
    o.Order_date,
    o.Shipping_address,
    o.Order_price
FROM `Order` o
JOIN Cake c         ON o.Cake_id = c.Cake_id
JOIN Customer cu    ON c.Customer_id = cu.Customer_id;

-- Usage:
SELECT * FROM vw_Order_Details;
SELECT * FROM vw_Order_Details WHERE Customer_name = 'Alice Johnson';


-- ----------------------------
-- View 2: vw_Invoice
-- Purpose: Generates a clean, customer-facing invoice layout.
--          Used at checkout or when emailing order confirmations.
-- ----------------------------
CREATE OR REPLACE VIEW vw_Invoice AS
SELECT
    o.Order_id                          AS Invoice_Number,
    cu.Customer_name                    AS Billed_To,
    cu.Customer_email                   AS Email,
    cu.Customer_phone                   AS Phone,
    CONCAT(c.Layers, '-Layer ',
           c.Cake_shape, ' ',
           c.Cake_batter, ' Cake')      AS Cake_Description,
    CONCAT(c.Side_frosting, ' sides / ',
           c.Top_frosting, ' top')      AS Frosting,
    CONCAT(c.Decoration_1,
           CASE WHEN c.Decoration_2 IS NOT NULL
                THEN CONCAT(', ', c.Decoration_2)
                ELSE ''
           END)                         AS Decorations,
    o.Order_occasion,
    o.Order_date,
    o.Shipping_address,
    o.Order_price                       AS Amount_Due
FROM `Order` o
JOIN Cake c         ON o.Cake_id = c.Cake_id
JOIN Customer cu    ON c.Customer_id = cu.Customer_id;

-- Usage:
SELECT * FROM vw_Invoice;
SELECT * FROM vw_Invoice WHERE Invoice_Number = 2;


-- ----------------------------
-- View 3: vw_Production_Schedule
-- Purpose: Shows upcoming orders sorted by date so bakers
--          can plan their daily production queue.
-- ----------------------------
CREATE OR REPLACE VIEW vw_Production_Schedule AS
SELECT
    o.Order_date,
    o.Order_id,
    cu.Customer_name,
    o.Order_occasion,
    c.Cake_shape,
    c.Cake_batter,
    c.Layers,
    c.Side_frosting,
    c.Top_frosting,
    c.Decoration_1,
    COALESCE(c.Decoration_2, 'None') AS Decoration_2,
    o.Shipping_address
FROM `Order` o
JOIN Cake c         ON o.Cake_id = c.Cake_id
JOIN Customer cu    ON c.Customer_id = cu.Customer_id
ORDER BY o.Order_date ASC;

-- Usage:
SELECT * FROM vw_Production_Schedule;
SELECT * FROM vw_Production_Schedule WHERE Order_date = '2025-04-12';


-- ----------------------------
-- View 4: vw_Revenue_Summary
-- Purpose: Management-level view summarizing revenue broken
--          down by occasion type and date.
-- ----------------------------
CREATE OR REPLACE VIEW vw_Revenue_Summary AS
SELECT
    Order_occasion,
    Order_date,
    COUNT(Order_id)             AS Orders_That_Day,
    SUM(Order_price)            AS Daily_Revenue,
    ROUND(AVG(Order_price), 2)  AS Avg_Order_Price
FROM `Order`
GROUP BY Order_occasion, Order_date
ORDER BY Order_date;

-- Usage:
SELECT * FROM vw_Revenue_Summary;
SELECT * FROM vw_Revenue_Summary WHERE Order_occasion = 'Birthday';


-- ----------------------------
-- View 5: vw_Customer_Order_History
-- Purpose: Shows every order placed per customer along with
--          a count of total orders — useful for loyalty tracking.
-- ----------------------------
CREATE OR REPLACE VIEW vw_Customer_Order_History AS
SELECT
    cu.Customer_id,
    cu.Customer_name,
    cu.Customer_email,
    COUNT(o.Order_id)           AS Total_Orders,
    SUM(o.Order_price)          AS Lifetime_Spend,
    MAX(o.Order_date)           AS Last_Order_Date
FROM Customer cu
LEFT JOIN Cake c    ON cu.Customer_id = c.Customer_id
LEFT JOIN `Order` o ON c.Cake_id = o.Cake_id
GROUP BY cu.Customer_id, cu.Customer_name, cu.Customer_email
ORDER BY Lifetime_Spend DESC;

-- Usage:
SELECT * FROM vw_Customer_Order_History;
SELECT * FROM vw_Customer_Order_History WHERE Customer_name = 'Bob Martinez';

-- ============================================================
--  END OF BAKERY MANAGEMENT SYSTEM SQL SCRIPT
-- ============================================================
