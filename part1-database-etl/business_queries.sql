# Query 1: Customer Purchase History

# Generate a detailed report showing 
# each customer's name, email, total number of orders placed, and total amount spent. 
# Include only customers who have placed at least 2 orders and 
# spent more than ₹5,000. Order by total amount spent in descending order."

# Expected to return customers with 2+ orders and >5000 spent

select  
CONCAT (a.first_name,'',a.last_name) as customer_name, a.email, 
count(b.order_id) as total_order, 
sum(b.total_amount) as total_spent  
from customers a INNER JOIN orders b on a.customer_id= b.customer_id 
group by 1,2 having total_spent > 5000 
order by total_spent DESC

# Query 2: Product Sales Analysis

# show the category name, number of different products sold, total quantity sold, and total revenue generated. 
# Only include categories that have generated more than ₹10,000 in revenue. 
# Order by total revenue descending."

# Expected to return categories with >10000 revenue

select p.category, count(distinct ito.product_id) as num_products, sum(ito.quantity) as total_quantity_sold, sum(ito.subtotal) as total_revenue
from products p INNER JOIN order_items ito on p.product_id = ito.product_id 
group by 1 having total_revenue>10000 
order by total_revenue DESC

# "Query 3: Monthly Sales Trend

# For each month, display 
# the month name, total number of orders, total revenue, and 
# the running total of revenue (cumulative revenue from January to that month)."
# month_name | total_orders | monthly_revenue | cumulative_revenue

# Expected to show monthly and cumulative revenue

select 
month_name, total_order, monthly_revenue, sum(monthly_revenue) over (order by order_date) 
from 
(select 
month(o.order_date) as order_date,
MONTHNAME(o.order_date) as month_name, 
sum(ito.quantity) as total_order,
sum(o.total_amount) as monthly_revenue 
from orders o inner join order_items ito 
group by 1,2) c






