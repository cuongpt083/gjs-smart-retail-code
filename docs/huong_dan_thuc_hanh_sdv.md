# Hướng dẫn thực hành: Giả lập dữ liệu KiotViet (Dành cho người mới)

Tài liệu này giúp các bạn hiểu cách sử dụng bộ công cụ (Jupyter Notebook) để tự tạo ra bộ dữ liệu bán lẻ (Grocery) tương thích với KiotViet mà không cần giỏi lập trình.

---

## 1. Lý thuyết cơ bản: Bạn đang làm gì?

Trong quản lý dữ liệu chuyên nghiệp, chúng ta không để tất cả thông tin vào một bảng duy nhất. Chúng ta chia làm 2 loại:

*   **Bảng Dimension (DIM - Danh mục)**: Chứa các thông tin "tĩnh" và ít thay đổi. Ví dụ: Danh sách Sản phẩm, Tên Khách hàng, Thông tin Nhân viên. Đây là nền móng của hệ thống.
*   **Bảng Fact (Sự kiện/Giao dịch)**: Chứa các thông tin phát sinh liên tục. Ví dụ: Hóa đơn bán hàng. Một dòng trong bảng Fact sẽ "trỏ" tới các bảng DIM (Ai mua? Mua cái gì?).

**Mục tiêu của chúng ta**: Dùng thuật toán để sinh ra hàng ngàn dòng dữ liệu trông như thật nhưng không bị lộ thông tin cá nhân của khách hàng thật.

---

## 2. Chuẩn bị môi trường

Trước khi bắt đầu, hãy đảm bảo bạn đã chọn đúng "Kernel" (môi trường chạy Python).
1. Mở notebook trong VS Code.
2. Nhìn vào góc trên bên phải màn hình.
3. Chọn **Select Kernel** -> **Python Environments** -> Chọn môi trường có tên `.venv` hoặc `gsjenv` (là nơi đã cài sẵn các thư viện cần thiết như Pandas, SDV).

---

## 3. Quy trình thực hành (3 Bước)

Bạn cần chạy các file theo đúng thứ tự từ **01 đến 03**:

### Bước 1: Sinh dữ liệu danh mục ([01_generate_dim_data.ipynb](file:///home/cuongpt/Workspaces/gjs-smart-retail-code/src/01_generate_dim_data.ipynb))
*   **Lý thuyết**: Notebook này đọc các file Excel mẫu và "học" cấu trúc. Sau đó nó dùng thư viện **Faker** để đổi tên người, tên quận huyện sang dữ liệu tại Hà Nội, Việt Nam.
*   **Thực hành**: Bạn chỉ cần nhấn nút **Run All**.
*   **Kết quả**: Bạn sẽ thấy các file `DIM_PRODUCTS_Import.xlsx`... xuất hiện trong thư mục `data/out/excel`.

### Bước 2: Sinh dữ liệu giao dịch ([02_generate_fact_data.ipynb](file:///home/cuongpt/Workspaces/gjs-smart-retail-code/src/02_generate_fact_data.ipynb))
*   **Lý thuyết**: Sau khi có Sản phẩm và Khách hàng ở Bước 1, notebook này sẽ giả lập việc "đi chợ". Nó sẽ chọn ngẫu nhiên một ngày trong tháng, chọn một khách hàng và một vài món hàng để tạo thành 1 hóa đơn.
*   **Quy tắc**: Mã hóa đơn luôn bắt đầu bằng `HDIP` (để KiotViet nhận diện được).
*   **Thực hành**: Nhấn **Run All**.
*   **Kết quả**: File `FACT_INVOICES_Full.xlsx` được tạo ra.

### Bước 3: Kiểm tra chất lượng ([03_quality_assurance.ipynb](file:///home/cuongpt/Workspaces/gjs-smart-retail-code/src/03_quality_assurance.ipynb))
*   **Lý thuyết**: Đây là bước "hậu kiểm". Nếu ở Bước 2 bạn lỡ bán 100 gói mỳ mà ở Bước 1 kho chỉ có 10 gói, KiotViet sẽ báo lỗi. Notebook này sẽ tự động kiểm tra và "điền thêm" hàng vào kho cho khớp.
*   **Thực hành**: Nhấn **Run All**.
*   **Kết quả**: Bạn sẽ có bộ dữ liệu cuối cùng hoàn toàn sạch lỗi nghiệp vụ.

---

## 4. Kiểm tra thành quả

Vào thư mục `data/out/excel/`, bạn sẽ thấy các file sẵn sàng để Import:
1. Import file **DIM_PRODUCTS** trước (để có hàng trong kho).
2. Sau đó mới Import file **FACT_INVOICES** (để ghi nhận bán hàng).

---
**Ghi chú**: Đừng sợ nếu thấy code báo lỗi đỏ, hãy kiểm tra lại xem mình đã chọn đúng Kernel ở Bước 2 chưa nhé!
