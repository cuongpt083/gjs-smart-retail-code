# 3 Phân tích mẫu dữ liệu đã thu thập

## 3.1 Dữ liệu khách hàng

Mẫu excel trả về từ hệ thống KiotViet có dạng sau:

### 3.1.1 Phân tích các đặc trưng của bộ dữ liệu khách hàng

- Mỗi dòng là một khách hàng riêng biệt, được phân biệt bởi Mã khách hàng
- Có 01 cột phái sinh (được sinh ra, tổng hợp ra từ các cột khác): đó là cột Tổng bán (Không import), lý do đưa ra nhận định này bởi vì cột này không được phép import data, mà có thể nó được tính dựa vào tổng giá trị các hóa đơn mà Khách hàng này đã mua.
- Kiểu dữ liệu:
  - Ngày sinh, Ngày giao dịch cuối: kiểu Date-time
  - Nợ cần thu hiện tại: Numeric
  - Tổng bán: Numeric
  - Trạng thái: Integer,  phỏng đoán rằng nếu là 1 thì thông tin Khách hàng này đang kích hoạt, 0 là Không kích hoạt.
  - Các trường thông tin còn lại: varchar (xâu ký tự độ dài không cố định)

Từ hai yếu tố trên, suy ra file Excel này ánh xạ 1:1 với một bảng dữ liệu Khách hàng, bảng này chứa các trường thông tin như trong file Excel. Bảng này được xem là một Master-Data, bởi vì dù hệ thống KiotViet có phát sinh giao dịch hay không, thì khách hàng và thông tin của khách hàng vẫn tồn tại trên thực tế, không biến mất.
Với đặc thù một hệ thống Kho dữ liệu trên thực tế (Data warehouse), bảng này sẽ là một Dimension table – tức là một bảng mô tả, danh mục, thông tin tham chiếu, ta sẽ quy ước tên bảng này là DIM_CUSTOMERS.

### 3.1.2 Đề xuất cấu trúc dữ liệu của bảng DIM_CUSTOMERS

Dựa trên template Excel và các phân tích ở trên, chúng ta có thể đề xuất như sau:

- Primary key: customer_code = Mã khách hàng
- Các cột thông tin (gắn với template Excel):
  - customer_type = Loại khách
  - customer_name = Tên khách hàng
  - phone = Điện thoại
  - address = Địa chỉ
  - area = Khu vực giao hàng
  - ward = Phường / Xã
  - company = Công ty
  - tax_code = Mã số thuế

## 3.2 Dữ liệu nhân viên

Mẫu Excel trả về từ hệ thống KiotViet có dạng như sau:

### 3.2.1 Phân tích các đặc trưng của bộ dữ liệu Nhân viên

Mỗi dòng là một bộ thông tin về một nhân viên duy nhất, được đại diện bởi Mã nhân viên

- Kiểu dữ liệu:
  - Mức lương: numeric
  - Ngày sinh, ngày bắt đầu làm việc: date-time
  - Các trường thông tin còn lại: varchar
- Không có các dòng/cột phái sinh
- Các cột bắt buộc phải có thông tin: Tên nhân viên, Số điện thoại -> dự đoán rằng Mã nhân viên được hệ thống tự động sinh ra.

Tương tự như đã phân tích với bảng Dữ liệu Khách hàng, bảng dữ liệu Nhân viên này là một bảng Master-data, cụ thể là một Dimension table chứa danh mục Nhân viên. Ta sẽ quy ước tên bảng này là DIM_EMPLOYEE, các trường thông tin liên quan đến Nhân viên được thể hiện tương tự như các cột trong file Excel.

### 3.2.2 Đề xuất cấu trúc của bảng DIM_EMPLOYEE

- Primary key: employee_code = Mã nhân viên
- Các trường khác liên quan tới template Excel:
  - employee_code (PK)
  - employee_name (Tên nhân viên)
  - phone (Số điện thoại)
  - department (Phòng ban)
  - title (Chức danh)
  - login (Tài khoản đăng nhập)
  - branch_working (Chi nhánh làm việc…)

Khi import hóa đơn, trường Người bán thường sẽ ánh xạ tới employee_name hoặc employee_code, do đó bạn nên thử với lượng dữ liệu nhỏ để kiểm chứng.

## 3.3 Dữ liệu Sản phẩm (hàng hóa, dịch vụ)

Mẫu file Excel trả về từ hệ thống KiotViet có dạng như sau:

### 3.3.1 Phân tích các đặc trưng của bộ dữ liệu Hàng hóa

- Mỗi dòng là một loại sản phẩm (bao gồm cả hàng hóa để bán và dịch vụ cung cấp cho khách hàng), định danh bởi Mã hàng, mã vạch. Mỗi sản phẩm bao gồm nhiều trường thông tin được thể hiện trong file Excel. SKU chính là Mã hàng bởi nó có tính duy nhất, các trường còn lại là thuộc tính mô tả của SKU.
- Kiểu dữ liệu của các trường thông tin:
  - Giá bán, Giá vốn: numeric
  - Tồn kho, Tồn nhỏ nhất, Tồn lớn nhất, Quy đổi: integer
  - Trọng lượng: integer
  - Đang kinh doanh, Được bán trực tiếp: boolean
  - Các thuộc tính còn lại: varchar
- SKU được diễn giải bởi tập hợp các trường thông tin: Mã hàng, Tên hàng, Thương hiệu, ĐVT (đơn vị tính), Thuộc tính

Bảng sản phẩm này vẫn tồn tại trên cửa hàng dù hệ thống KiotViet có hoạt động hay không, do đó nó là một Master-data, cụ thể là một Dimension table chứa danh mục các Sản phẩm của cửa hàng. Ta sẽ quy ước tên bảng này là DIM_PRODUCTS.

### 3.3.2 Đề xuất cấu trúc của bảng DIM_PRODUCTS

- Primary key: product_code = “Mã hàng”
- Các cột khác dựa trên template Excel:
  - product_type = Loại hàng
  - category_path = Nhóm hàng(3 Cấp)
  - product_code = Mã hàng (PK)
  - barcode = Mã vạch (unique, có thể để null một phần)
  - product_name = Tên hàng
  - brand = Thương hiệu
  - sale_price = Giá bán
  - cost_price = Giá vốn
  - stock_on_hand = Tồn kho (cực quan trọng để pass rule tồn kho)
  - uom = ĐVT
  - is_active = Đang kinh doanh
  - is_direct_sale = Được bán trực tiếp

## 3.4 Dữ liệu đơn hàng

### 3.4.1 Một số khái niệm cơ bản

Đơn hàng là kết quả của một giai đoạn trong quá trình bán hàng. Dựa trên các dữ liệu được kết xuất ra từ Excel của hệ thống KiotViet, quá trình bán hàng sẽ sản sinh ra 03 loại dữ liệu sau:

- Đơn đặt hàng (order): là giai đoạn khách hàng đang dự định mua hàng, mục tiêu là giữ chỗ hàng hóa, số lượng và chủng loại hàng hóa trong đơn đặt hàng có thể được thay đổi hoặc hủy bỏ và chưa phát sinh thanh toán cho cửa hàng.
- Hóa đơn (invoice): là kết quả của giao dịch, trong đó hàng hóa/dịch vụ đã được lựa chọn, xử lý, thanh toán và có thể bao gồm cả giao hàng. Mục tiêu của hóa đơn là ghi nhận doanh thu.
- Do hóa đơn có rất nhiều thông tin bao gồm: thông tin người bán, thông tin người mua, thông tin sản phẩm, thông tin thanh toán, thông tin giao hàng, cho nên trong thực tế, không bao giờ chúng ta tổ chức lưu trữ một bảng hóa đơn khổng lồ chứa toàn bộ thông tin này, mà luôn luôn tách biệt lưu trữ thành các bảng nhỏ hơn rồi tham chiếu tới chúng.

### 3.4.2 Phân tích các đặc trưng của bộ dữ liệu Đơn hàng

Mẫu file Excel trả về từ KiotViet như sau:

- Danh sách chi tiết đặt hàng (Orders)

- File danh sách các hóa đơn

Thông tin đơn đặt hàng, hóa đơn này chỉ tồn tại trên hệ thống KiotViet, nó là kết quả của các giao dịch, do đó trong một hệ thống Data Warehouse thì các bảng này được xem là các bảng Facts (ghi thông tin hóa đơn, giao dịch, sự kiện).  
Căn cứ trên các phân tích đã thực hiện, chúng ta sẽ tổ chức dữ liệu Hóa đơn thành 2 bảng FACT_INVOICES chứa thông tin hóa đơn và FACT_INVOICES_LINES chứa thông tin chi tiết của hóa đơn bao gồm các trường phái sinh, foreign key tham chiếu tới bảng FACT_INVOICES. Tương tự, chúng ta cũng sẽ có 2 bảng FACT_ORDERS chứa thông tin đơn đặt hàng và FACT_ORDERS_LINES chứa thông tin chi tiết đơn đặt hàng bao gồm các trường phái sinh và các foreign key tham chiếu tới bảng FACT_ORDERS.

### 3.4.3 Đề xuất cấu trúc của bảng FACT_INVOICES

- Primary key: invoice_code (PK, format HDIPxxxxx)
- Các trường thông tin khác liên quan tới template Excel:
  - invoice_time =  thời gian
  - seller = Người bán (FK logic tới employees)
  - sales_channel = Kênh bán
  - customer_code (FK tới DIM_CUSTOMERS)
  - pricebook = Bảng giá (optional)
  - invoice_discount_amount = Giảm giá hóa đơn
  - invoice_discount_percent = Giảm giá hóa đơn %
  - pay_cash = Tiền mặt
  - pay_card = Thẻ
  - pay_transfer = Chuyển khoản
  - note = Ghi chú

### 3.4.4 Đề xuất cấu trúc của bảng FACT_INVOICES_LINES

- Primary key: invoice_line_id
- Các trường thông tin khác liên quan template Excel:
  - invoice_code (FK)  tham chiếu tới invoice_code ở bảng FACT_INVOICES
  - product_code = Mã hàng (FK)
  - quantity = Số lượng
  - unit_price = Đơn giá
  - line_discount_percent = Giảm giá %
  - line_discount_amount = Giảm giá

Một số khuyến nghị để đảm bảo việc import dễ dàng hơn:

- Hạn chế sử dụng SDV để sinh unit_price ngẫu nhiên, hãy thiết lập unit_price = sale_price
- Quantity nên là số dương, thường thì ở tiệm tạp hóa người ta sẽ mua từ 1-5 món.

### 3.4.5 Đề xuất cấu trúc của bảng FACT_ORDERS

- Primary key: order_code
- Các trường thông tin khác:
  - order_time = Thời gian
  - customer_code / customer_name
  - amount_due = Khách cần trả
  - amount_paid = Khách đã trả
  - status = Trạng thái

Trong phạm vi khóa học này, chúng ta không quá quan tâm tới nghiệp vụ giao nhận trong quá trình bán hàng, do đó chúng ta bỏ qua các thông tin liên quan tới giao nhận hàng hóa, các giao dịch đều là mua hàng trực tiếp.

### 3.4.6 Đề xuất cấu trúc của bảng FACT_ORDERS_LINES

- Primary key: order_line_id
- Foreign key: order_code  ánh xạ sang trường order_code của bảng FACT_ORDERS
- Các trường thông tin khác:
  - product_code = Mã hàng (FK)
  - barcode (optional)
  - product_name (optional; có thể derive)
  - quantity
  - unit_price
  - discount_percent
  - discount_amount
  - line_total = Thành tiền (khuyến nghị tính lại sau)

### 3.5 Các ràng buộc nghiệp vụ phát hiện được trong quá trình phân tích dữ liệu mẫu

#### 3.5.1 Rule R1 – Mã hóa đơn có prefix HDIP

Trong quá trình mở giao diện import danh sách hóa đơn, màn hình có ghi chú rằng mã hóa đơn phải có prefix HDIP, trường hợp bỏ trống thì hệ thống sẽ tự sinh mã hóa đơn. Do vậy trong quá trình định nghĩa metadata/constraint cho SDV, chúng ta cần thực hiện:

- “invoice_code”: phải có dạng HDIPXXXX trong đó XXXX là các số tăng dần

#### 3.5.2 Rule R2 – Tồn kho đủ

Trong giao diện import hóa đơn, logic có ghi rõ, số lượng trong hóa đơn phải nhỏ hơn số lượng hàng đang tồn kho, do đó việc thiết lập logic cần đảm bảo như sau:

- Đặt DIM_PRODUCTS.stock_on_hand đủ lớn ngay từ đầu (giả lập số lượng khi nhập hàng, ví dụ 200-500 sản phẩm), hoặc:
- Nếu muốn thật hơn, sau khi SDV sinh invoice_lines, thực hiện chạy bước hậu xử lý:
  - Cộng tổng quantity theo product
  - Thiết lập stock_on_hand >= tổng đã bán + dự trữ

#### 3.5.3 Rule R3 – Thời gian, số lượng, tiền thanh toán hợp lệ

- Quantity > 0
- Unit_price >= 0
- Discount >= 0
- Thanh toán: pay_cash + pay_card + pay_transfer gần bằng “tổng cần thu”. Cách an toàn đó là tính lại payment sau khi tính tổng hóa đơn.

#### 3.5.4 Rule R4 – Khóa ngoại tồn tại

- “Mã hàng” trong invoice/order phải tồn tại trong DIM_PRODUCTS
- “Mã KH” trong excel nếu dùng thì phải có dữ liệu DIM_CUSTOMERS
