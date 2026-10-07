# E-Commerce Sales Data Engineering Pipeline

An end-to-end data engineering project that transforms raw e-commerce transaction data into a clean analytical dataset, SQLite database, SQL insights, and an interactive Power BI dashboard.

The project demonstrates practical data engineering concepts including **ETL, data cleaning, validation, transformation, SQL analytics, database loading, and business intelligence reporting** using Python, Pandas, SQLite, SQL, and Power BI.

---

## Project Overview

This project processes raw e-commerce transaction data through a structured data pipeline:

**Raw CSV → Python/Pandas ETL → Data Validation & Cleaning → Processed CSV → SQLite Database → SQL Analysis → Power BI Dashboard**

The goal is to build a reproducible workflow where raw transactional data can be transformed into reliable data products for analysis and reporting.

---

## Architecture

```text
                 ┌─────────────────────────┐
                 │      Raw CSV Data       │
                 │ Online Retail Dataset   │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │   Python / Pandas ETL   │
                 │                         │
                 │ • Remove duplicates     │
                 │ • Handle missing data   │
                 │ • Validate values       │
                 │ • Calculate revenue     │
                 │ • Create Month field    │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │   Cleaned Sales CSV     │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │      SQLite Database    │
                 │      ecommerce_sales    │
                 └────────────┬────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
          ┌─────────────────┐   ┌──────────────────┐
          │  SQL Analysis   │   │  Power BI        │
          │                 │   │  Dashboard       │
          │ • Revenue       │   │                  │
          │ • Orders        │   │ • KPIs           │
          │ • Products      │   │ • Countries      │
          │ • Customers     │   │ • Products       │
          │ • Daily Sales   │   │ • Customers      │
          └─────────────────┘   └──────────────────┘
```

---

## Tech Stack

| Technology | Purpose                                 |
| ---------- | --------------------------------------- |
| Python     | Data pipeline and automation            |
| Pandas     | Data cleaning and transformation        |
| SQLite     | Local analytical database               |
| SQL        | Data analysis and aggregation           |
| Power BI   | Interactive dashboard and visualization |
| Git        | Version control                         |
| GitHub     | Source code and project documentation   |
| VS Code    | Development environment                 |

---

## Dataset

The project uses an e-commerce transaction dataset containing information about:

* Invoice numbers
* Product codes
* Product descriptions
* Quantities
* Invoice dates
* Unit prices
* Customer IDs
* Countries

The current project uses a **5,000-row sample** of the transaction data.

The dataset represents actual transactional records used by the pipeline. No artificial sales months or business values were added.

---

## ETL Pipeline

### 1. Extract

The pipeline reads the raw CSV file from:

```text
data/raw/Online_Retail_5000_Rows.csv
```

Python and Pandas are used to load the raw transaction data.

---

### 2. Transform

The pipeline performs several data quality and transformation operations:

* Removes duplicate records
* Cleans text fields
* Converts `InvoiceDate` into datetime format
* Converts numerical columns into appropriate numeric types
* Removes records missing essential fields
* Removes transactions with invalid quantities
* Removes transactions with invalid unit prices
* Calculates transaction revenue
* Creates a month field for analytical aggregation

Revenue is calculated as:

```text
Revenue = Quantity × UnitPrice
```

---

### 3. Load

The cleaned dataset is stored as:

```text
data/processed/cleaned_sales.csv
```

The processed data is then loaded into a SQLite database:

```text
database/ecommerce_sales.db
```

The database contains the analytical `sales` table.

---

## Data Quality Results

The pipeline processes the raw dataset and reports data quality statistics.

| Metric                                    | Result |
| ----------------------------------------- | -----: |
| Raw Rows                                  |  5,000 |
| Duplicate Rows Removed                    |     79 |
| Rows Removed for Missing Essential Values |     12 |
| Invalid Quantity/Price Rows Removed       |     70 |
| Final Clean Rows                          |  4,839 |

The pipeline validates the database after loading to confirm that the expected number of records has been inserted and that revenue values are positive.

---

## Business Results

After cleaning and transformation, the pipeline produces:

| KPI                 |       Value |
| ------------------- | ----------: |
| Total Revenue       | £103,763.71 |
| Total Units Sold    |      56,182 |
| Total Orders        |         259 |
| Unique Customers    |         179 |
| Unique Products     |       1,579 |
| Countries           |           7 |
| Average Order Value |     £400.63 |

---

## SQL Analysis

The project includes a reusable SQL analysis file:

```text
sql/analysis.sql
```

The SQL analysis covers:

1. Total revenue
2. Total units sold
3. Total orders
4. Unique customers
5. Unique products
6. Revenue by country
7. Top 10 products by revenue
8. Top 10 customers by revenue
9. Monthly sales performance
10. Average order value
11. Daily revenue
12. Highest revenue orders

SQL queries are executed through:

```text
src/run_sql.py
```

---

## Power BI Dashboard

The processed data is also used to create an interactive Power BI dashboard.

Dashboard file:

```text
powerbi/ecommerce_sales_dashboard.pbix
```

### Dashboard includes

* Total Revenue
* Total Orders
* Total Units Sold
* Unique Customers
* Unique Products
* Revenue by Country
* Top 10 Products by Revenue
* Daily Revenue
* Top 10 Customers by Revenue
* Country Performance table

### Dashboard Preview

Add a screenshot of the Power BI dashboard here after uploading it to GitHub.

```text
docs/dashboard-preview.png
```

---

## Project Structure

```text
ecommerce-sales-data-pipeline/
│
├── data/
│   ├── raw/
│   │   └── Online_Retail_5000_Rows.csv
│   │
│   └── processed/
│       └── cleaned_sales.csv
│
├── database/
│   └── ecommerce_sales.db
│
├── output/
│   ├── overall_kpis.csv
│   ├── monthly_summary.csv
│   ├── country_summary.csv
│   ├── product_summary.csv
│   ├── customer_summary.csv
│   └── sales_summary.csv
│
├── powerbi/
│   └── ecommerce_sales_dashboard.pbix
│
├── sql/
│   └── analysis.sql
│
├── src/
│   ├── pipeline.py
│   ├── load_database.py
│   └── run_sql.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/palak-thakur10/ecommerce-sales-data-pipeline.git
```

### 2. Open the project

```bash
cd ecommerce-sales-data-pipeline
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the ETL pipeline

```bash
python src/pipeline.py
```

This creates the cleaned dataset and analytical output files.

### 5. Load the data into SQLite

```bash
python src/load_database.py
```

This creates:

```text
database/ecommerce_sales.db
```

### 6. Run SQL analysis

```bash
python src/run_sql.py
```

The script executes the SQL queries from:

```text
sql/analysis.sql
```

### 7. Open the Power BI dashboard

Open:

```text
powerbi/ecommerce_sales_dashboard.pbix
```

using Power BI Desktop.

---

## Key Data Engineering Concepts Demonstrated

This project demonstrates practical experience with:

* ETL pipeline development
* Data ingestion
* Data cleaning
* Data validation
* Data transformation
* Data quality checks
* Data aggregation
* Relational database loading
* SQL analytics
* Reproducible processing
* Analytical data preparation
* Business intelligence reporting
* Version-controlled project structure

---

## Limitations

The current implementation uses a **5,000-row sample dataset** and SQLite for local analytical processing.

The dataset available for this project contains transactions from December 2010 in the current sample, so the dashboard does not artificially create a multi-month sales trend.

The project is intentionally focused on building a reliable **data engineering workflow at sample scale** rather than claiming a production-scale Big Data platform.

---

## Future Improvements

Potential extensions include:

* PySpark-based distributed data processing
* Automated data validation tests
* Incremental data loading
* Partitioned datasets
* Cloud-based data storage
* Scheduled pipeline execution
* Data warehouse integration
* Docker-based deployment
* Automated CI/CD pipeline
* Larger datasets for performance testing

These improvements would extend the project toward larger-scale data engineering workflows.

---

## Author

**Palak Thakur**

BCA Graduate | Data Engineering & Software Development Enthusiast

GitHub:
https://github.com/palak-thakur10

---

## Project Focus

**Python • Pandas • SQL • SQLite • Power BI • ETL • Data Engineering • Data Analytics**
