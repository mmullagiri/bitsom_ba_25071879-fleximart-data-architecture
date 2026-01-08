1. Entity relationship description: 

ENTITY: customers
Purpose: Stores customer information
Attributes:
  - customer_id: Unique identifier (Primary Key)
  - first_name: Customer's first name
  - last_name: Customer's last name
  - email: Customer's email ID
  - phone: Customer's phone number
  - city: Customer's city
  - registration_date: Date when Customer registered with the store

ENTITY: products
Purpose: Stores product information
Attributes:

  - product_id: Identifies each product uniquely.
  - product_name: Stores the name of the product.
  - category: Indicates the category or type the product belongs to.
  - price: Represents the selling price of the product.
  - stock_quantity: Shows how many units of the product are currently available in inventory.
  

ENTITY: orders
Purpose: Stores orders information
Attributes:
  - order_id: Identifies each order uniquely.
  - customer_id: Customer ID of the customer who placed the order.
  - order_date: Stores the date when the order was placed.
  - total_amount: Represents the total cost of the order.
  - status: Shows the current state of the order (such as pending, completed, or cancelled).

ENTITY: order_items
Purpose: Stores order details
Attributes:
  - order_item_id: Identifies each line item within an order uniquely.
  - order_id: Links the items to the order it belongs to.
  - product_id: Identifies the product ID of the item included in the order.
  - quantity: Indicates how many units of the product were ordered.
  - unit_price: Represents the price of a single unit of the product at the time of ordering.
  - subtotal: Shows the total cost for this order item (quantity × unit price).

Relationships:
  - One customer can place MANY orders (1:M with orders table)
  - One order can contain MANY order items (1:M with order_items table)
  - A product can appear in many order items but each order item refers to just 1 product (1:M with order_items table)
  - An order can include many products and a product can feature in many orders (M:N between products and orders)

2. Normalization explanation: 

2a. Explain why this design is in 3NF (200-250 words)
This design is in 3NF because it eliminates data redundancy, and every non-key attribute depends only on the primary key and nothing else. 
1 NF satisfied: 
    Each field contains single, indivisible value. And each record is uniquely identified by the primary key
2 NF satisfied: 
    non-key atributes fully dependent on primary key. Even in Order_items, each non-key attribute such as quantity, unit_price or subtotal is dependent on specific order_item.
3 NF satisfied: 
    No transitive dependencies. Non-key attributes do not depend on other non-key attributes. 

2b. Identify functional dependencies
Functional dependencies for each table: 
CUSTOMER TABLE: 
    customer_id ---> first_name, last_name, email, phone, city, registration_date
PRODUCTS TABLE:
    product_id ---> product_name, category, price, stock_quantity
ORDERS TABLE:
    order_id ---> customer_id, order_date, total_amount, status
ORDER_ITEMS TABLE:
    order_item_id ---> order_id, product_id, quantity, unit_price, subtotal
    (order_id, product_id) ---> quantity, unit_price, subtotal
    
2c. Explain how the design avoids update, insert, and delete anomalies
By separating customers, products, orders, and order items into distinct entities, the design ensures data integrity, minimizes redundancy, and makes updates, insertions, and deletions more reliable and efficient.
Insert anomalies are avoided because new data can be added independently for entity tables as customers, products. And for Orders and Order Items, new data can be inserted only when the referencing product and customer Ids and order IDs exist.
Delete nomalies are avoided as removing one type of data does not unintentionally remove other important information. example: Deleting an order does not delete the customer’s record. Each entity is stored independently, with relationships managed through foreign keys
Update anomalies are avoided because each piece of information is stored in only one place. Therefore any updates to be made are to be made only in one place. And every other place where that information is referenced will then be able to fetch the updated data. 

3. Sample data representation: 
Showing below are 2-3 records from each table: 

ORDER ITEMS table:
order_item_id	order_id	product_id	quantity	unit_price	subtotal
    1	            1	        1	        1	        45999	    45999
    2	            2	        4	        2	        2999	    5998
    3	            3	        7	        1	        52999	    52999

ORDERS table: Corresponding Order IDs from order table are below:
order_id	customer_id	order_date	total_amount	status
    1            1	    2024-01-15	    45999	    Completed
    2            2	    2024-01-16	    5998	    Completed
    3            3	    2024-01-15	    52999	    Completed

Corresponding customer IDs from customer table are below
customer_id	first_name	last_name	email	            phone	        city	registration_date
    1	        Rahul	Sharma	rahul.sharma@gmail.com	91-9876543210	Bangalore	2023-01-15
    2	        Priya	Patel	priya.patel@yahoo.com	91-9988776655	Mumbai	    2023-02-20
    3	        Amit	Kumar	C003@flexmart.com	    91-9765432109	Delhi	    2023-03-10

PRODUCTS table: Corresponding Product IDs from Product table are below:
product_id	product_name	    category	    price	stock_quantity
    1	    Samsung Galaxy S21	Electronics	    45999	    150
    4	    Levi's Jeans	    Fashion	        2999	    120
    7	    HP Laptop	        Electronics	    52999	    60


