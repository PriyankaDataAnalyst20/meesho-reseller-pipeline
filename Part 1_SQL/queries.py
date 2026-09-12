import sqlite3
import csv
import os

# Connect to database
db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'meesho_reseller.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Create output directory
output_dir = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(output_dir, exist_ok=True)

# Query 1: Monthly revenue by category
print("Query 1: Monthly revenue by category...")
cur.execute("""
    SELECT 
        month,
        category,
        ROUND(SUM(quantity * unit_price), 2) as revenue,
        COUNT(*) as n_orders
    FROM orders
    GROUP BY month, category
    ORDER BY month, category
""")
results = cur.fetchall()
with open(os.path.join(output_dir, 'monthly_category_revenue.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['month', 'category', 'revenue', 'n_orders'])
    writer.writerows(results)
print(f"✓ Saved {len(results)} rows")

# Query 2: Region-wise revenue
print("Query 2: Region-wise revenue...")
cur.execute("""
    SELECT 
        r.region,
        ROUND(SUM(o.quantity * o.unit_price), 2) as revenue,
        COUNT(o.order_id) as n_orders
    FROM orders o
    JOIN resellers r ON o.reseller_id = r.reseller_id
    GROUP BY r.region
    ORDER BY revenue DESC
""")
results = cur.fetchall()
with open(os.path.join(output_dir, 'region_wise_revenue.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['region', 'revenue', 'n_orders'])
    writer.writerows(results)
print(f"✓ Saved {len(results)} rows")

# Query 3: Top resellers by spend
print("Query 3: Top resellers by spend...")
cur.execute("""
    SELECT 
        r.reseller_id,
        r.reseller_name,
        ROUND(SUM(o.quantity * o.unit_price), 2) as total_spend
    FROM orders o
    JOIN resellers r ON o.reseller_id = r.reseller_id
    GROUP BY r.reseller_id
    HAVING total_spend > 50000
    ORDER BY total_spend DESC
    LIMIT 5
""")
results = cur.fetchall()
with open(os.path.join(output_dir, 'top_resellers_by_spend.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['reseller_id', 'reseller_name', 'total_spend'])
    writer.writerows(results)
print(f"✓ Saved {len(results)} rows")

# Query 4a: Zero-order resellers
print("Query 4a: Zero-order resellers...")
cur.execute("""
    SELECT 
        r.reseller_id,
        r.reseller_name,
        r.region
    FROM resellers r
    LEFT JOIN orders o ON r.reseller_id = o.reseller_id
    WHERE o.order_id IS NULL
""")
results = cur.fetchall()
with open(os.path.join(output_dir, 'zero_order_resellers.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['reseller_id', 'reseller_name', 'region'])
    writer.writerows(results)
print(f"✓ Saved {len(results)} rows")

# Query 4b: COUNT(*) vs COUNT(order_id) demonstration
print("Query 4b: COUNT demonstration for RS024...")
cur.execute("""
    SELECT 
        r.reseller_id,
        COUNT(*) as count_all,
        COUNT(o.order_id) as count_order_id
    FROM resellers r
    LEFT JOIN orders o ON r.reseller_id = o.reseller_id
    WHERE r.reseller_id = 'RS024'
    GROUP BY r.reseller_id
""")
results = cur.fetchall()
with open(os.path.join(output_dir, 'count_demonstration.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['reseller_id', 'count_all', 'count_order_id'])
    writer.writerows(results)
print(f"✓ Saved {len(results)} rows")
print("  Note: COUNT(*) = 1, COUNT(order_id) = 0 (shows why COUNT(*) is wrong)")

# Query 5: AOV for June, Delivered
print("Query 5: AOV for June, Delivered...")
cur.execute("""
    SELECT 
        ROUND(SUM(quantity * unit_price) / COUNT(*), 2) as aov
    FROM orders
    WHERE month = 'June' AND status = 'Delivered'
""")
result = cur.fetchone()
with open(os.path.join(output_dir, 'aov_june_delivered.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['aov'])
    writer.writerow(result)
print(f"✓ Saved AOV value: {result[0]}")

# Query 6: Grand total revenue verification
print("Query 6: Grand total revenue verification...")
cur.execute("""
    SELECT 
        ROUND(SUM(quantity * unit_price), 2) as grand_total_revenue
    FROM orders
""")
result = cur.fetchone()
with open(os.path.join(output_dir, 'grand_total_revenue.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['grand_total_revenue'])
    writer.writerow(result)
print(f"✓ Grand total: {result[0]}")

conn.close()
print("\n✅ All queries completed!")

conn.close()
print("\n✅ All queries completed! Check part1_sql/output/ for CSV files")