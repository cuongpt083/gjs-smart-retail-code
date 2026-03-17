# SDV Pipeline Implementation Plan

This document outlines the detailed steps and technical approach for building the Synthetic Data Vault (SDV) pipeline to generate data for the KiotViet system.

## Proposed Changes

We will create three Jupyter Notebooks in the `src/` directory to handle different aspects of the data generation process.

### src/00_common_utils.ipynb

This notebook will contain shared utility functions and configurations.

- [NEW] `src/00_common_utils.ipynb`
  - Implement dynamic header detection for Excel files.
  - Create mapping dictionaries between Excel template columns and canonical database schema columns.
  - Implement validation functions (e.g., checking UUID formatting, ensuring foreign keys exist).
  - Create chunking logic to export large datasets into smaller Excel files (e.g., 1000 rows per file for KiotViet import limits).
  - Setup logging configuration and common project paths (e.g., `templates/`, `warehouse/`, `sdv-out/`).

### src/01_generate_dim_data.ipynb

This notebook will generate the master data (Dimensions): Customers, Employees, and Products.

- [NEW] `src/01_generate_dim_data.ipynb`
  - **Setup:** Import `00_common_utils.ipynb` functions. Define required record counts (e.g., 1000 customers, 50 employees, 500 products).
  - **Products (DIM_PRODUCTS):** Use Faker and rule-based logic to generate realistic product data. Ensure `stock_on_hand` is sufficiently high (e.g., 200-500) to pass later inventory checks. Enforce realistic pricing rules (e.g., `sale_price >= cost_price`).
  - **Customers (DIM_CUSTOMERS):** Generate customer profiles with realistic Vietnamese names, phone numbers, and addresses.
  - **Employees (DIM_EMPLOYEES):** Generate employee data with realistic roles and branches.
  - **Export:** Save the generated dimension tables as timestamped CSV snapshots in `warehouse/` and formatted Excel files for system import in `sdv-out/excel/`.

### src/02_generate_fact_data.ipynb

This notebook will generate transaction data (Facts): Orders and Invoices, ensuring referential integrity with the generated dimensions.

- [NEW] `src/02_generate_fact_data.ipynb`
  - **Setup:** Load the latest snapshot CSVs from `warehouse/` (Products, Customers, Employees). Stop execution if dimension data is missing.
  - **Parameters:** Define configuration for generation, such as date range, transactions per day, basket size distribution (e.g., 1-5 items per invoice), and payment method distribution.
  - **Generation Logic:**
    - Construct `FACT_INVOICES` holding header-level information (Customer, Employee, Time, Payments). Ensure `invoice_code` follows the `HDIPxxxxx` format.
    - Construct `FACT_INVOICES_LINES` ensuring `product_code` exists in `DIM_PRODUCTS`. Retrieve `unit_price` from the dimension table. Ensure total payment amounts match line totals.
  - **Export:** Chunk the output files if exceeding 1000 rows. Export as Excel files in `sdv-out/excel/` and CSV files in `warehouse/`. Create a SQLite database (`warehouse/retail_synthetic.db`) and load the dimensional and fact data for further analysis.

## Verification Plan

### Automated Tests

- Run all three notebooks sequentially.
- Verify that output files exist in the expected directories (`warehouse/` and `sdv-out/excel/`).
- Query the SQLite database to confirm all required tables exist and contain the expected number of rows.
- Verify referential integrity within the SQLite DB (e.g., no orphaned invoice lines).

### Manual Verification

- Manually inspect a sample of the generated Excel files to ensure headers match the KiotViet templates exactly.
- Check generated data for realism (e.g., positive prices, valid phone formats, reasonable names).
- If possible, attempt a test import of generated Excel files into a sandbox KiotViet environment to validate structural compliance.
