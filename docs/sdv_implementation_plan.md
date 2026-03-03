# SDV Implementation Plan

## Table of Contents

- [Introduction](#introduction)
- [Implementation Steps](#implementation-steps)
- [Configuration](#configuration)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)

## Introduction

Quá trình giả lập dữ liệu sử dụng SDV (Synthetic Data Vault) bao gồm các bước sau:

- Tạo 02 jupyter notebook để giả lập dữ liệu cho các bảng dữ liệu trong vault:
  - 01_generate_dim_data.ipynb: tạo dữ liệu cho các bảng dimension trong data warehouse, cụ thể là các bảng dim_customers, dim_products, dim_employees.
  - 02_generate_fact_data.ipynb: tạo dữ liệu cho các bảng fact trong data warehouse, cụ thể là bảng fact_orders, fact_orders_lines, fact_invoices, fact_invoices_lines.
- Tạo 01 utils notebook `00_common_utils.ipynb` để tạo các hàm chung cho các jupyter notebook:
  - hàm detect header row trong file Excel
  - mapping cột template <-> canonical
  - validator PK/FK, chunk exporter 200 dòng
  - logger, config loader
- Các DIM notebook sẽ xuất ra snapshot version (ví dụ dim_products_v1.csv, dim_products_v2.csv, ...)
- Các FACT notebook sẽ luôn đọc theo các DIM snapshot version được chọn. Mỗi lần chạy FACT:
  - sinh FACT mới theo date range
  - ghi log: tham số, seed, số bản ghi, thời gian chạy

## Implementation Steps

### Notebook DIM

#### 1. Setup & config

- Khai báo đường dẫn:
  - `template/`: Excel template của KiotViet
  - `out/excel`: file import dữ liệu sinh bởi SDV lên hệ thống của KiotViet
  - `out/csv`: file import dữ liệu sinh bởi SDV vào data warehouse
  - `warehouse/`: thư mục chứa các file dim snapshot, metadata, logs, SQLite database (giả lập data warehouse)
- Config tham số:
  - số lượng sản phẩm, khách hàng, nhân viên
  - seed random
  - tỷ lệ missing (email, barcode, ...)
  - danh sách category, brand, uom mẫu

#### 2. Read & profile Excel templates (reverse-engineering)

- Đọc các file `MauFileSanPham.xlsx`, `MauFileKhachHang.xlsx`, `MauFileImportNhanVien.xlsx` để hiểu cấu trúc của các bảng dimension.
- Tự động thực hiện:
  - detect header row
  - lấy danh sách cột template
  - đoán kiểu dữ liệu của mỗi cột template (numeric, date, categorical, datetime)
  - đoán cột "id-like" (PK/FK) của mỗi bảng template (Mã hàng, Mã KH, Mã NV, Barcode)
  - đoán mối quan hệ giữa các bảng template
- Output: data dictionary (markdown file) + "schema proposal" bản nháp

#### 3. Build DIM schema (canonical tables)

- Chuẩn hoá tên cột nội bộ (snake_case) nhưng lưu mapping sang cột tiếng Việt template
- Chốt PK:
  - product_code, customer_code, employee_code
- Chốt unique candidates:
  - barcode (nếu dùng), phone (tuỳ)

#### 4. Generate DIM data (2 chế độ)

- Mode 1: Faker/rule-based (khuyến nghị cho lần đầu, không cần data thật)
  - generate sản phẩm theo ngành hàng, brand, uom, giá bán/giá vốn hợp lý
  - generate khách hàng theo khu vực/phường ở Hà Nội (hoặc generic)
  - generate nhân viên + vai trò
- Mode 2: SDV “augment” (khi có dữ liệu thật/seed):
  - fit SDV từ mẫu nhỏ (nếu bạn có)
  - sample để mở rộng

#### 5. Business constraints cho DIM (enforce/validate)

- Products:
  - price >= 0, cost >=0, (thường cost <= price)
  - stock_on_hand >= 0
  - is_active tỷ lệ ~80–95%
- barcode format/length (nếu có)
- Employees:
  - phone format, unique (tuỳ)
  - required fields không null
- Customers:
  - phone format, optional email
- Report: số lượng trùng PK, trùng barcode/phone, tỷ lệ null

#### 6. Export outputs

- Excel import KiotViet:
  - điền đúng sheet + đúng thứ tự cột theo template
- CSV chuẩn hoá:
  - dim_products.csv, dim_customers.csv, dim_employees.csv
- Snapshot versioning:
  - lưu dim_snapshot_YYYYMMDD.csv
  - Lưu config: dim_config.json (seed, params)

#### 7. Quick sanity dashboards (nhỏ gọn)

- histogram giá bán, giá vốn, tồn kho
- top categories/brands
- kiểm tra phân bố uom

### Notebook FACT `02_generate_fact_data.ipynb`

#### 1. Setup & Load DIM snapshot

- Load dim_products.csv, dim_customers.csv, dim_employees.csv
- Nếu thiếu DIM → cảnh báo “chạy notebook 01 trước”

#### 2. Read & profile transaction templates (reverse-engineering)

- Đọc MauFileDanhSachHoaDon.xlsx (InvoiceTemplate)
- Đọc DanhSachDatHang_*.xlsx + DanhSachChiTietDatHang_*.xlsx

- Tự động:
  - Phát hiện cột header vs line
  - Gợi ý bảng:
    - fact_invoices, fact_invoice_lines
    - fact_orders, fact_order_lines
  - Phát hiện các cột “derived” (thành tiền, khách cần trả…)

#### 3. Define FACT generation plan (scenario-based)

Cho học sinh chọn scenario bằng tham số:

- date_range (ví dụ 2026-03-01 → 2026-03-31)
- số hoá đơn/ngày
- tỷ lệ:
  - bán tại quầy vs giao hàng
  - cash/card/transfer
  - có khách hàng vs khách lẻ
  - basket size (số dòng/hoá đơn)
  - promo/discount rate

#### 4. Generate headers + lines (khuyến nghị rule-based + SDV tuỳ mức)

- Rule-based core (đảm bảo logic):
  - chọn customer (hoặc null), seller
  - chọn sản phẩm theo popularity (Zipf) + category mix
  - quantity distribution (1–5 chủ yếu)
  - unit_price lấy từ dim_products.sale_price (± noise nhỏ)
- SDV bổ trợ (nếu có data seed):
  - fit multi-table để học phân phối giờ bán, kênh bán, discount…

#### 5. Enforce business constraints (critical)

- Hóa đơn:
  - invoice_code bắt đầu bằng HDIP
  - mỗi invoice có >=1 line
- Lines:
  - product_code phải tồn tại trong DIM
  - quantity > 0, unit_price >= 0
  - discount% trong [0,100]
- Thanh toán:
  - tính tổng tiền từ lines
  - phân bổ vào cash/card/transfer sao cho khớp
- Orders:
  - order có thể chưa có invoice (tuỳ trạng thái)
  - COD logic (nếu bạn mô phỏng)

#### 6. Inventory post-processing (để import KiotViet không fail)

Có 2 chiến lược (chọn 1):

- Strategy A (dễ, ổn định cho lớp học):
  - set tồn kho DIM ban đầu rất lớn (500–2000/sp)
  - không cần trừ tồn trong FACT, chỉ cần “đủ”
- Strategy B (thật hơn):
  - tính tổng bán theo product_code
  - nếu bán vượt tồn:
    - tăng tồn kho (để import pass)
    - hoặc giảm bớt quantity (để giữ tồn kho cố định)
  - xuất ra file products cập nhật tồn kho nếu cần

#### 7. Validate “import readiness”

- Check-list trước khi export Excel:
  - số dòng <= 1000 cho InvoiceTemplate (chunk nếu vượt)
  - không null ở cột bắt buộc (*)
  - mã hàng tồn tại
  - date hợp lệ
  - Xuất report lỗi (CSV + markdown)

#### 8. Export outputs

- Excel import KiotViet
  - Invoices_001.xlsx, Invoices_002.xlsx… (chunk 1000 lines)
- (tuỳ mục tiêu) Orders.xlsx, OrderDetails.xlsx dạng export để học sinh phân tích
- CSV cho SQLite/ML
  - fact_invoices.csv
  - fact_invoice_lines.csv
  - fact_orders.csv
  - fact_order_lines.csv

#### 9. Load to SQLite (phục vụ bài ML)

- Tạo SQLite db (vd: retail_synthetic.db)
- Tạo tables + indexes (PK/FK)
- Import CSV vào SQLite
- Quick queries:
  - doanh thu theo ngày
  - top SKU
  - RFM đơn giản

### Notebook Utils

Các chức năng chính trong đó:

- hàm detect header row excel
- mapping cột template ↔ canonical
- validator PK/FK, chunk exporter 1000 dòng
- logger & config loader

## Configuration

## Usage

## Troubleshooting
