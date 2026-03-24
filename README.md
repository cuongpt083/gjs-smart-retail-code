# GSJ Smart Retail Code

Source code cho dự án **GSJ Smart Retail**.

Dự án này chuyên trách việc mô phỏng, khởi tạo và quản lý dữ liệu cho hệ thống bán lẻ (Smart Retail), mô phỏng dữ liệu giống với thực tế và xuất ra dưới dạng báo cáo định dạng chuẩn của KiotViet, cũng như lưu trữ dưới cấu trúc Data Warehouse (CSV, SQLite) nhằm mục đích phân tích dữ liệu và xây dựng Dashboard.

## Cấu trúc thư mục

- `src/`: Chứa các script giả lập dữ liệu (Jupyter Notebook).
  - `00_common_utils.ipynb`: Các hàm dùng chung (utils), ánh xạ cấu trúc cột dữ liệu tương thích với KiotViet.
  - `01_generate_dim_data.ipynb`: Script sinh dữ liệu danh mục (Dimensions) bao gồm Hệ thống sản phẩm, Khách hàng, Nhân viên dựa trên danh mục thực tế.
  - `02_generate_fact_data.ipynb`: Script sinh dữ liệu giao dịch (Facts) bao gồm Hóa đơn và Chi tiết hóa đơn với các ràng buộc để đảm bảo toàn vẹn dữ liệu.
- `docs/`: Chứa các tài liệu triển khai dự án, kế hoạch thực hiện thuật toán SDV, và các prompt tham chiếu thiết kế cấu trúc Dashboard.
- `templates/`: Các tệp mẫu `.xlsx` chuẩn (được lấy từ KiotViet) dùng làm đầu vào để mô phỏng cấu trúc cột hàng cho dữ liệu.
- `warehouse/`: Thư mục lưu trữ dữ liệu Data Warehouse mô phỏng sau khi chạy sinh dữ liệu đầu ra `.csv` và cơ sở dữ liệu `retail_synthetic.db` (SQLite).
- `sdv-out/`: Thư mục lưu trữ dữ liệu xuất ra dưới định dạng `.xlsx` đã được chia nhỏ thành từng chunk nhằm phục vụ tác vụ import vào KiotViet.
- `pipelines/` & `data/`: Thư mục chuẩn bị cho việc xây dựng Data pipelines và thao tác tính toán Data Engineering sau này.

## Quy trình sử dụng

1. **Khởi tạo dữ liệu danh mục:**
   Khởi chạy `src/01_generate_dim_data.ipynb` để sinh ra dữ liệu Sản phẩm, Khách hàng, Nhân viên.
2. **Khởi tạo dữ liệu giao dịch:**
   Khởi chạy `src/02_generate_fact_data.ipynb` để sinh ra dữ liệu Hóa đơn (Invoices, Invoice Lines). Dữ liệu này sẽ tự động map (khớp) với tập khách hàng, nhân viên và sản phẩm đã tạo trước đó.
3. **Sử dụng Dữ liệu:**
   - Để nạp vào hệ thống phần mềm (ví dụ: KiotViet): Lấy files trong mục `sdv-out/excel/`.
   - Để xây dựng nền tảng dữ liệu báo cáo BI (PowerBI/Tableau/Metabase): Lấy file `.db` hoặc `.csv` từ đường dẫn `warehouse/`.
