---
title: GJS Smart Retail - Dashboard & ETL Validation Design
author: GJS Team
date: 2026-03-24
---

# Thiết Kế Chi Tiết: Retail Dashboard & Kiểm Thử ETL Pipeline

Tài liệu này định nghĩa các đặc tả cần thiết để xây dựng một Dashboard phân tích bán lẻ (Retail Analytics Dashboard). Mục đích chính của Dashboard này, bên cạnh việc cung cấp góc nhìn kinh doanh, là **trực quan hóa và kiểm chứng tính đúng đắn của dữ liệu (Data Quality & Validation)** được sinh ra từ quy trình ETL hiện tại (các script `01_generate_dim_data` và `02_generate_fact_data`).

---

## 1. Mục Tiêu Kiểm Thử ETL Thông Qua Dashboard

Dashboard sẽ đóng vai trò như một công cụ Data Quality Check (DQC) trực quan. Việc dữ liệu hiển thị đúng trên biểu đồ sẽ chứng minh pipeline ETL hoạt động chính xác. Các điểm cần kiểm chứng bao gồm:

*   **Tính Toàn vẹn Tham chiếu (Referential Integrity):** Không có giao dịch `FACT_INVOICES` nào bị "mồ côi" (thiếu `customer_code`, `employee_code` hoặc `product_code` không tồn tại trong tập DIM).
*   **Ràng buộc Logic Toán học (Mathematical Logic):** `total_amount` trên Invoice bắt buộc phải khớp với `SUM(line_total)` của các Invoice Lines tương ứng.
*   **Tính Nhất quán Dữ liệu (Data Consistency):** Giá bán (`unit_price`) trong chi tiết hóa đơn khớp với `sale_price` trong bảng sản phẩm tại thời điểm bán; không có giá trị Null ở các trường quan trọng (Mã, Giá, Số lượng).
*   **Phân phối Dữ liệu (Data Distribution):** Dữ liệu giả lập mô phỏng đúng tính ngẫu nhiên (số lượng đơn hàng theo ngày, sự đa dạng của phương thức thanh toán...).

---

## 2. Đặc Tả Dữ Liệu Đầu Vào (Nguồn Dữ Liệu)

*   **Nguồn:** Database SQLite (`warehouse/retail_synthetic.db`)
*   **Cấu trúc bảng (Schema):**
    *   `DIM_PRODUCTS` (Mã SP, Tên SP, Nhóm hàng, Giá vốn, Giá bán, Tồn kho)
    *   `DIM_CUSTOMERS` (Mã KH, Tên, Số điện thoại, Địa chỉ)
    *   `DIM_EMPLOYEES` (Mã NV, Tên, Vai trò, Chi nhánh)
    *   `FACT_INVOICES` (Mã HĐ, Mã KH, Mã NV, Thời gian, Tổng tiền, Hình thức thanh toán)
    *   `FACT_INVOICES_LINES` (Mã HĐ, Mã SP, Số lượng, Đơn giá, Thành tiền)

---

## 3. Kiến Trúc Dashboard & Các Metrics Cụ Thể

Dashboard được chia thành 3 màn hình/tab chính, phục vụ các khía cạnh kiểm tra khác nhau:

### Tab 1: Executive Summary & ETL Sanity Checks (Tổng quan số liệu & Cảnh báo lỗi)
*Trang này tập trung vào các KPI chính và các chỉ báo lỗi dữ liệu trực tiếp.*

*   **KPI Scorecards (Thẻ điểm):**
    *   Tổng số Đơn hàng (Invoices Count).
    *   Tổng Doanh thu (Sum of Total Amount).
    *   Tổng Khách hàng đã giao dịch.
*   **ETL Error Alerts (Cảnh báo lỗi dữ liệu - Quan trọng):**
    *   *Số lượng hóa đơn lệch tổng tiền:* Đếm số `invoice_code` mà `FACT_INVOICES.total_amount != SUM(FACT_INVOICES_LINES.line_total)`. (Kỳ vọng = 0).
    *   *Số lượng Missing Dimension:* Số lượng transaction mapping ra Null categories. (Kỳ vọng = 0).

### Tab 2: Sales & Time-Series Analysis (Phân tích theo thời gian & Hoạt động)
*Trang này dùng để kiểm tra sự phân bổ tính ngẫu nhiên của tập dữ liệu Fact được tạo ra trong khoảng thời gian N ngày.*

*   **Doanh thu & Số lượng đơn hàng theo thời gian (Line Chart / Stacked Bar Chart):**
    *   Trục X: Ngày giao dịch.
    *   Trục Y1 (Bar): Số lượng đơn. Trục Y2 (Line): Tổng doanh thu.
    *   *ETL Check:* Đảm bảo dữ liệu trượt đều theo mô phỏng (50-150 đơn/ngày), không có "hole" (khoảng trống ngày không có data).
*   **Tỷ trọng Phương thức thanh toán (Pie Chart/Donut Chart):**
    *   *ETL Check:* Kiểm tra xem script sinh random "Tiền mặt", "Chuyển khoản", "Thẻ" có hoạt động và phân bổ tự nhiên không.
*   **Biểu đồ Nhiệt Giờ Vàng (Heatmap):** Điểm danh số đơn hàng theo Khung Giờ và Ngày trong tuần.

### Tab 3: Dimensions Analysis (Phân Tích Chi Tiết Đối Tượng)
*Trang này tập trung vào kiểm tra mức độ đa dạng của dữ liệu Master Data.*

*   **Doanh thu theo Nhóm sản phẩm (Treemap):** Phân bổ Top 1, Top 2 category. Nguồn: `DIM_PRODUCTS.category`.
*   **Doanh số & Đơn hàng theo Chi nhánh (Horizontal Bar Chart):**
    *   *ETL Check:* Khẳng định `DIM_EMPLOYEES.branch` map chính xác với lượng hóa đơn mà mỗi nhân viên đó phụ trách.
*   **Cảnh báo tồn kho giả lập (Scatter Plot):**
    *   Tốc độ bán ra vs. Tồn kho (`stock_on_hand`).

---

## 4. Đặc Tả Triển Khai (Technology & Execution)
*(Được thiết kế dưạ trên nguyên lý SMART POLE Framework nhằm định hướng rõ rệt cho Coding Agent bước tiếp theo)*

*   **[S] Style:** Sử dụng Python thuần. Mã nguồn module hóa rõ ràng (Tách biệt Data Loading logic và UI Rendering).
*   **[L] Locale (Ecosystem):** 
    *   Môi trường: Python.
    *   Thư viện lõi UI: **Streamlit** (tối ưu cho data app).
    *   Thư viện biểu diễn: **Plotly** (interactive charts), **Pandas** (xử lý dataframe).
*   **[A] Aim (Mục tiêu nghiệm thu):**
    *   Chạy lệnh `streamlit run dashboard.py` thành công.
    *   Kết nối trực tiếp vào `warehouse/retail_synthetic.db`.
    *   Tất cả các thành phần biểu đồ trên 3 Tab render phản hồi nhanh (dưới 3s), không văng lỗi ngoại lệ.
*   **[O] Outline (Phạm vi):**
    *   Tạo file mới: `src/03_dashboard.py` (hoặc `src/dashboard_app.py`).
    *   Tạo file `requirements.txt` cập nhật thêm `streamlit`, `plotly` nếu chưa có.
    *   Chỉ SELECT (.sql queries) từ database có sẵn. KHÔNG INSERT hay UPDATE lại dữ liệu.

---
*Tài liệu này đóng vai trò là Blueprint cho bước xây dựng ứng dụng trực quan hóa tiếp theo trên dữ liệu Warehouse.*
