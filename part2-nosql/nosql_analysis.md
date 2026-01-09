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