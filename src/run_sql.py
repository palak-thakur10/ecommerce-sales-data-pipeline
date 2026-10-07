from pathlib import Path
import sqlite3


# Project root folder
BASE_DIR = Path(__file__).resolve().parent.parent

# File paths
DATABASE_PATH = BASE_DIR / "database" / "ecommerce_sales.db"
SQL_PATH = BASE_DIR / "sql" / "analysis.sql"


# Connect to SQLite database
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()


# Read SQL file
sql_text = SQL_PATH.read_text(encoding="utf-8")


# Split queries using semicolon
queries = [
    query.strip()
    for query in sql_text.split(";")
    if query.strip()
]


print("=" * 60)
print("SQL ANALYSIS RESULTS")
print("=" * 60)


# Run each query
for number, query in enumerate(queries, start=1):

    print(f"\n--- Query {number} ---")
    print(query)

    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        print(row)


# Close database
conn.close()

print("\n" + "=" * 60)
print("SQL ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)