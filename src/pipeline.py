import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "Online_Retail_5000_Rows.csv"
)

PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "output"

CLEANED_FILE = PROCESSED_DIR / "cleaned_sales.csv"


# ============================================================
# EXTRACT
# ============================================================

def extract_data():
    """Load raw e-commerce transaction data."""

    print("\n[EXTRACT]")
    print("Loading raw dataset...")

    df = pd.read_csv(RAW_FILE)

    print(f"Raw rows: {len(df):,}")
    print(f"Raw columns: {len(df.columns)}")

    return df


# ============================================================
# TRANSFORM
# ============================================================

def transform_data(df):
    """Clean and transform transaction data."""

    print("\n[TRANSFORM]")
    print("Cleaning data...")

    # --------------------------------------------------------
    # Remove duplicate transactions
    # --------------------------------------------------------

    before = len(df)

    df = df.drop_duplicates()

    duplicates_removed = before - len(df)

    print(f"Duplicates removed: {duplicates_removed:,}")

    # --------------------------------------------------------
    # Clean text columns
    # --------------------------------------------------------

    df["Description"] = (
        df["Description"]
        .astype("string")
        .str.strip()
    )

    df["Country"] = (
        df["Country"]
        .astype("string")
        .str.strip()
    )

    # --------------------------------------------------------
    # Convert data types
    # --------------------------------------------------------

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"],
        errors="coerce"
    )

    df["Quantity"] = pd.to_numeric(
        df["Quantity"],
        errors="coerce"
    )

    df["UnitPrice"] = pd.to_numeric(
        df["UnitPrice"],
        errors="coerce"
    )

    df["CustomerID"] = pd.to_numeric(
        df["CustomerID"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Remove rows missing essential transaction information
    # --------------------------------------------------------

    required_columns = [
        "InvoiceNo",
        "StockCode",
        "Description",
        "InvoiceDate",
        "Quantity",
        "UnitPrice",
        "Country"
    ]

    before = len(df)

    df = df.dropna(
        subset=required_columns
    )

    print(
        f"Rows removed because of missing "
        f"essential values: {before - len(df):,}"
    )

    # --------------------------------------------------------
    # Keep valid sales transactions
    # --------------------------------------------------------

    before = len(df)

    df = df[
        (df["Quantity"] > 0)
        & (df["UnitPrice"] > 0)
    ]

    print(
        f"Invalid quantity/price rows removed: "
        f"{before - len(df):,}"
    )

    # --------------------------------------------------------
    # Create Revenue column
    # --------------------------------------------------------

    df["Revenue"] = (
        df["Quantity"] * df["UnitPrice"]
    ).round(2)

    # --------------------------------------------------------
    # Create Month column
    # --------------------------------------------------------

    df["Month"] = (
        df["InvoiceDate"]
        .dt.to_period("M")
        .astype(str)
    )

    print(f"Clean rows: {len(df):,}")

    return df


# ============================================================
# LOAD - PROCESSED CSV
# ============================================================

def save_cleaned_data(df):
    """Save cleaned transaction data."""

    print("\n[LOAD]")
    print("Saving processed dataset...")

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        CLEANED_FILE,
        index=False
    )

    print(
        f"Saved: {CLEANED_FILE}"
    )


# ============================================================
# ANALYTICAL SUMMARIES
# ============================================================

def generate_summaries(df):
    """Generate analytical summary CSV files."""

    print("\n[ANALYSIS]")
    print("Generating summary datasets...")

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Overall KPIs
    # --------------------------------------------------------

    total_revenue = df["Revenue"].sum()

    total_units = df["Quantity"].sum()

    total_orders = df["InvoiceNo"].nunique()

    unique_products = df["StockCode"].nunique()

    unique_customers = df["CustomerID"].nunique()

    unique_countries = df["Country"].nunique()

    average_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )

    overall_kpis = pd.DataFrame({
        "Metric": [
            "Total Revenue",
            "Total Units",
            "Total Orders",
            "Unique Products",
            "Unique Customers",
            "Countries",
            "Average Order Value"
        ],
        "Value": [
            round(total_revenue, 2),
            int(total_units),
            int(total_orders),
            int(unique_products),
            int(unique_customers),
            int(unique_countries),
            round(average_order_value, 2)
        ]
    })

    overall_kpis.to_csv(
        OUTPUT_DIR / "overall_kpis.csv",
        index=False
    )

    # --------------------------------------------------------
    # Monthly Summary
    # --------------------------------------------------------

    monthly_summary = (
        df.groupby("Month")
        .agg(
            Revenue=("Revenue", "sum"),
            Units=("Quantity", "sum"),
            Orders=("InvoiceNo", "nunique"),
            Customers=("CustomerID", "nunique")
        )
        .reset_index()
        .sort_values("Month")
    )

    monthly_summary["Revenue"] = (
        monthly_summary["Revenue"]
        .round(2)
    )

    monthly_summary.to_csv(
        OUTPUT_DIR / "monthly_summary.csv",
        index=False
    )

    # --------------------------------------------------------
    # Country Summary
    # --------------------------------------------------------

    country_summary = (
        df.groupby("Country")
        .agg(
            Revenue=("Revenue", "sum"),
            Units=("Quantity", "sum"),
            Orders=("InvoiceNo", "nunique")
        )
        .reset_index()
        .sort_values(
            "Revenue",
            ascending=False
        )
    )

    country_summary["Revenue"] = (
        country_summary["Revenue"]
        .round(2)
    )

    country_summary.to_csv(
        OUTPUT_DIR / "country_summary.csv",
        index=False
    )

    # --------------------------------------------------------
    # Product Summary
    # --------------------------------------------------------

    product_summary = (
        df.groupby(
            ["StockCode", "Description"],
            dropna=False
        )
        .agg(
            Units=("Quantity", "sum"),
            Revenue=("Revenue", "sum"),
            Orders=("InvoiceNo", "nunique")
        )
        .reset_index()
        .sort_values(
            "Revenue",
            ascending=False
        )
    )

    product_summary["Revenue"] = (
        product_summary["Revenue"]
        .round(2)
    )

    product_summary.to_csv(
        OUTPUT_DIR / "product_summary.csv",
        index=False
    )

    # --------------------------------------------------------
    # Customer Summary
    # --------------------------------------------------------

    customer_summary = (
        df.dropna(subset=["CustomerID"])
        .groupby("CustomerID")
        .agg(
            Revenue=("Revenue", "sum"),
            Units=("Quantity", "sum"),
            Orders=("InvoiceNo", "nunique")
        )
        .reset_index()
        .sort_values(
            "Revenue",
            ascending=False
        )
    )

    customer_summary["Revenue"] = (
        customer_summary["Revenue"]
        .round(2)
    )

    customer_summary.to_csv(
        OUTPUT_DIR / "customer_summary.csv",
        index=False
    )

    # --------------------------------------------------------
    # Sales Summary
    # --------------------------------------------------------

    sales_summary = (
        df.groupby("InvoiceNo")
        .agg(
            Revenue=("Revenue", "sum"),
            Units=("Quantity", "sum"),
            CustomerID=("CustomerID", "first"),
            InvoiceDate=("InvoiceDate", "first"),
            Country=("Country", "first")
        )
        .reset_index()
        .sort_values(
            "Revenue",
            ascending=False
        )
    )

    sales_summary["Revenue"] = (
        sales_summary["Revenue"]
        .round(2)
    )

    sales_summary.to_csv(
        OUTPUT_DIR / "sales_summary.csv",
        index=False
    )

    print("Summary files generated successfully.")

    print("\nMonthly distribution:")
    print(monthly_summary.to_string(index=False))


# ============================================================
# MAIN ETL PIPELINE
# ============================================================

def main():

    print("=" * 60)
    print("E-COMMERCE SALES DATA ENGINEERING PIPELINE")
    print("=" * 60)

    # Extract
    df = extract_data()

    # Transform
    df = transform_data(df)

    # Load
    save_cleaned_data(df)

    # Generate analytical datasets
    generate_summaries(df)

    print("\n" + "=" * 60)
    print("ETL PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()