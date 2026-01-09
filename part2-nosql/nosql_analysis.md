Section A: 
-------------------------
Limitation of current relational database:
1) Products having different attributes (e.g., laptops have RAM/processor, shoes have size/color)
    When need to store attributes of a product, we have 2 choices. Store the attribute details as a paragraph or understand the key attributes users are interested in and store them as distinct columns. Storing as a paragraph renders not much advantage when we want to compare features. 
    However the attribute list of each product type differ so widely. To think of a single table to store duch diverse and divergent attributes will warrant creating a lot of columns resulting the table will become sparse thereby wasting storage. Plus, this also will evidently be mixing unrelated data thereby violating normalization principles. One more approach can be to have separate tables for each product type but that will make querying difficult and managing the schema difficult. 
2) Frequent schema changes when adding new product types
    In either cases, with each new product type added, the schema changes will either include adding new columns (resorting to ALTER table) or adding new attribute table for new product type and establish new constrains. Both are risky. So it is clear that this schema design will struggle due to relational schemas being rigid and schema dependent and not suitable for evolving and variable product attributes. 
3) Storing customer reviews as nested data
    Storing customer reviews as nested data will incur several joins and complicate the storung and extraction leading to performance issues and system load that can be avoided. 

Section B: NoSQL Benefits
---------------------------------------------
Explain how MongoDB solves these problems:
Flexible schema (document structure):
1. MongoDB stores data as documents, structed like JSON, and each document can have a different structure. Key advantage being: No Fixed columns, for each product store only the attributes that are pertinent, therefore no wastage of storage for storing null values, and new products with their attributes can be added without disrupting the schema. 

2. Embedded documents (reviews within products)
Reviews for all products can be easily saved and collated. This is helpful not just reviews of products but also embedded documents to provide/represent next level of an attribute set for a certain product attribute.

3. Horizontal scalability
Relational databases scale vertically, while NoSQLs like MongoDB are designed for horizontal scalability. These adhere to the CAP theorem (consistency, availability, partition tolerance). 
To scale horizontally, NoSQLs rely on eventual consistency than strong consistency. This enables fast writes with lesser coordination. 
They natively support sharding. Since related data are stored together, joins and queries would be minimal, and queries normally hit a single shard. This works well for Partition tolerance.  
NoSQL replicate data across nodes, this facilitates higher availability

Section C:
---------------------------------
What are two disadvantages of using MongoDB instead of MySQL for this product catalog

1) Weaker schema enforcement, thereby causing data inconsistency. Not just data but also attribute naming inconsistency can occur. This will then mandate such logics are taken care/addressed in the application
2) Data aggregation and analysis become complex as queries across differing type of data structures for same kind of entity (product, in this case) will be tough unlike in the case of relational DB. This further flows down to analysis and reporting challenges too with noSQL DBs as MongoDB. 