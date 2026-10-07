import sqlite3
from pathlib import Path
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CLEANED_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "cleaned_sales.csv"
)

DATABASE_DIR = BASE_DIR / "database"

DATABASE_FILE = (
    DATABASE_DIR
    / "ecommerce_sales.db"
)


# ============================================================
# LOAD CSV
# ============================================================

def load_cleaned_data():
    """Load the cleaned transaction CSV."""

    print("\n[LOAD DATA]")
    print("Reading cleaned sales data...")

    df = pd.read_csv(
        CLEANED_FILE
    )

    print(f"Rows loaded: {len(df):,}")

    return df


# ============================================================
# CREATE DATABASE
# ============================================================

def create_database(df):
    """Create SQLite database and sales table."""

    print("\n[DATABASE]")
    print("Creating SQLite database...")

    DATABASE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    df.to_sql(
        "sales",
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()

    print(
        f"Database created successfully:"
    )
    print(DATABASE_FILE)


# ============================================================
# VERIFY DATABASE
# ============================================================

def verify_database():
    """Verify the SQLite database."""

    print("\n[VERIFY]")

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM sales"
    )

    row_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM sales WHERE Revenue > 0"
    )

    valid_revenue_rows = cursor.fetchone()[0]

    connection.close()

    print(
        f"Rows in database: {row_count:,}"
    )

    print(
        f"Rows with positive revenue: "
        f"{valid_revenue_rows:,}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("SQLITE DATA LOADING PIPELINE")
    print("=" * 60)

    df = load_cleaned_data()

    create_database(df)

    verify_database()

    print("\n" + "=" * 60)
    print("DATABASE LOAD COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()