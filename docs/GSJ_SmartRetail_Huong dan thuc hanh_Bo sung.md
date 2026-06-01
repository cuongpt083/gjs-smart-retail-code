# HƯỚNG DẪN THỰC HÀNH: PHÁT TRIỂN HỆ THỐNG PHÂN TÍCH BÁN LẺ THÔNG MINH (BỔ SUNG)

> **Lưu ý:** Tài liệu này bổ sung cho các phần còn thiếu trong hướng dẫn chính, tập trung vào việc thiết kế Data Warehouse, giả lập dữ liệu và xây dựng Dashboard.

---

## CHƯƠNG 0: CHUẨN BỊ MÔI TRƯỜNG

Để thực hiện dự án này, học sinh cần cài đặt môi trường lập trình Python và các thư viện hỗ trợ.

### 0.1 Cài đặt Python và Virtual Environment
1. Tải và cài đặt Python 3.11+.
2. Tạo môi trường ảo (Virtual Environment):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Trên Linux/Mac
   venv\Scripts\activate     # Trên Windows
   ```

### 0.2 Cài đặt thư viện cần thiết
Chạy lệnh sau để cài đặt các thư viện:
```bash
pip install streamlit pandas plotly openpyxl numpy faker sdv
```

---

## CHƯƠNG 4: THIẾT KẾ DATA WAREHOUSE (SQLITE)

Sau khi đã phân tích cấu trúc dữ liệu từ các tệp Excel của KiotViet (xem Chương 3), bước tiếp theo là thiết kế một cơ sở dữ liệu SQLite để lưu trữ dữ liệu này một cách tối ưu cho việc phân tích.

### 4.1 Cấu trúc các bảng Dimension (Bảng danh mục)

Các bảng này chứa thông tin ít thay đổi (Master Data).

#### 4.1.1 Bảng `DIM_CUSTOMERS`
| Tên cột | Kiểu dữ liệu | Ràng buộc | Diễn giải |
| --- | --- | --- | --- |
| `customer_code` | TEXT | PRIMARY KEY | Mã khách hàng (VD: KH0001) |
| `customer_name` | TEXT | NOT NULL | Tên khách hàng |
| `phone` | TEXT | | Số điện thoại |
| `address` | TEXT | | Địa chỉ |
| `area` | TEXT | | Khu vực giao hàng |
| `customer_type` | TEXT | | Loại khách (Cá nhân/Bán buôn) |

#### 4.1.2 Bảng `DIM_PRODUCTS`
| Tên cột | Kiểu dữ liệu | Ràng buộc | Diễn giải |
| --- | --- | --- | --- |
| `product_code` | TEXT | PRIMARY KEY | Mã hàng (SKU) |
| `product_name` | TEXT | NOT NULL | Tên sản phẩm |
| `category` | TEXT | | Nhóm hàng |
| `brand` | TEXT | | Thương hiệu |
| `sale_price` | REAL | | Giá bán |
| `cost_price` | REAL | | Giá vốn |
| `uom` | TEXT | | Đơn vị tính |
| `stock_on_hand`| INTEGER| | Tồn kho hiện tại |

#### 4.1.3 Bảng `DIM_EMPLOYEES`
| Tên cột | Kiểu dữ liệu | Ràng buộc | Diễn giải |
| --- | --- | --- | --- |
| `employee_code` | TEXT | PRIMARY KEY | Mã nhân viên |
| `employee_name` | TEXT | NOT NULL | Tên nhân viên |
| `phone` | TEXT | | Số điện thoại |
| `title` | TEXT | | Chức danh |

### 4.2 Cấu trúc các bảng Fact (Bảng giao dịch)

Các bảng này lưu trữ các sự kiện giao dịch phát sinh hàng ngày.

#### 4.2.1 Bảng `FACT_INVOICES` (Thông tin chung hóa đơn)
| Tên cột | Kiểu dữ liệu | Ràng buộc | Diễn giải |
| --- | --- | --- | --- |
| `invoice_code` | TEXT | PRIMARY KEY | Mã hóa đơn (Prefix: HDIP) |
| `timestamp` | DATETIME | | Thời gian giao dịch |
| `customer_code`| TEXT | FK -> DIM_CUSTOMERS| Khách hàng thực hiện |
| `employee_code`| TEXT | FK -> DIM_EMPLOYEES| Nhân viên bán hàng |
| `total_amount` | REAL | | Tổng tiền hóa đơn |
| `payment_method`| TEXT | | Tiền mặt/Thẻ/Chuyển khoản |

#### 4.2.2 Bảng `FACT_INVOICES_LINES` (Chi tiết hóa đơn)
| Tên cột | Kiểu dữ liệu | Ràng buộc | Diễn giải |
| --- | --- | --- | --- |
| `line_id` | INTEGER | PRIMARY KEY AUTOINC| ID dòng |
| `invoice_code` | TEXT | FK -> FACT_INVOICES | Tham chiếu hóa đơn |
| `product_code` | TEXT | FK -> DIM_PRODUCTS | Sản phẩm được mua |
| `quantity` | INTEGER | | Số lượng |
| `unit_price` | REAL | | Đơn giá bán |
| `line_total` | REAL | | Thành tiền (Qty * Price) |

---

## CHƯƠNG 5: GIẢ LẬP DỮ LIỆU BẰNG PYTHON (SDV & FAKER)

Trong chương này, học sinh sẽ sử dụng Python để sinh dữ liệu giả lập có ý nghĩa nghiệp vụ.

### 5.1 Sử dụng thư viện Faker cho Dữ liệu Dimension
Học sinh thực hiện trong file `01_generate_dim_data.ipynb`:
1. Khởi tạo `Faker('vi_VN')` để sinh tên người và số điện thoại Việt Nam.
2. Sinh danh sách Sản phẩm dựa trên các ngành hàng thực tế (Mỹ phẩm, Đồ gia dụng, v.v.).
3. Đảm bảo tính duy nhất của Primary Key.

### 5.2 Xây dựng Logic Giao dịch (Fact Data)
Học sinh thực hiện trong file `02_generate_fact_data.ipynb`:
1. **Phân bổ thời gian**: Sử dụng phân phối xác suất để sinh nhiều đơn hàng hơn vào các giờ cao điểm (11h-13h và 18h-21h).
2. **Logic giỏ hàng**: Mỗi hóa đơn có từ 1-5 sản phẩm ngẫu nhiên từ bảng `DIM_PRODUCTS`.
3. **Ràng buộc nghiệp vụ**:
   - `invoice_code` phải bắt đầu bằng `HDIP`.
   - `total_amount` phải bằng tổng của các `line_total`.
   - `stock_on_hand` của sản phẩm phải đủ để đáp ứng hóa đơn.

---

## CHƯƠNG 6: LẬP TRÌNH DASHBOARD PHÂN TÍCH VỚI STREAMLIT

Đây là bước cuối cùng để hiển thị kết quả phân tích cho người dùng nghiệp vụ.

### 6.1 Cấu trúc ứng dụng Streamlit
Học sinh thực hiện trong file `src/03_dashboard.py`:
- **Kết nối dữ liệu**: Sử dụng `sqlite3` và `pandas` để đọc dữ liệu từ tệp `.db`.
- **Thiết kế Layout**: Sử dụng `st.tabs` để chia dashboard thành các khu vực:
  - Tab 1: Tổng quan (Doanh thu, số đơn, kiểm tra lỗi dữ liệu).
  - Tab 2: Phân tích bán hàng (Biểu đồ đường theo thời gian).
  - Tab 3: Tồn kho & Sản phẩm (Top hàng bán chạy).
  - Tab 4: Phân khúc Marketing (RFM Analysis).

### 6.2 Triển khai Phân khúc RFM (Recency, Frequency, Monetary)
Học sinh cần lập trình các bước sau:
1. **Recency**: Tính số ngày kể từ lần mua cuối cùng của khách hàng.
2. **Frequency**: Tính tổng số đơn hàng khách đã mua.
3. **Monetary**: Tính tổng giá trị chi tiêu của khách hàng.
4. **Scoring**: Chia khách hàng thành 5 nhóm (Quintiles) cho mỗi chỉ số R, F, M.
5. **Mapping**: Sử dụng ma trận 5x5 để phân vào 11 nhóm (Champions, Loyal, Hibernating, v.v.).

### 6.3 Trực quan hóa dữ liệu
Sử dụng thư viện `Plotly` để tạo các biểu đồ tương tác:
- `px.line`: Diễn biến doanh thu.
- `px.pie`: Tỷ trọng phương thức thanh toán.
- `go.Heatmap`: Ma trận RFM 5x5.

---

## BÀI TẬP VỀ NHÀ
1. Hãy bổ sung thêm một Tab mới vào Dashboard để phân tích hiệu suất nhân viên bán hàng.
2. Thiết lập tính năng lọc dữ liệu theo "Khu vực" của khách hàng trong Tab RFM.
