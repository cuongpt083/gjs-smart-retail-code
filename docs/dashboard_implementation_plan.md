# Kế Hoạch Triển Khai: Dashboard Phân Khúc Khách Hàng RFM

> Tài liệu này ghi lại các quyết định thiết kế đã được thống nhất và hướng dẫn triển khai chi tiết cho Dashboard Module RFM. Là tài liệu companion cho `dashboard-pipeline-design.md`.

---

## I. Phân Tích Ngữ Cảnh (SMART POLE Framework)

| Phạm Trù | Nội Dung |
| --- | --- |
| **[S] Style** | Python thuần. Module hóa rõ ràng: tách hàm tính toán `perform_rfm_analysis()` khỏi UI rendering. Chú thích thân thiện Gen-Z. |
| **[M] Mastery** | *Domain*: Business/Data Analyst. *Task*: Kết hợp Pandas in-memory (`groupby`, `qcut`) với Streamlit Plotly interactive charts. |
| **[A] Aim** | Dashboard có **Tab 4** phục vụ riêng Marketing. Tính toán 11 nhóm RFM tiêu chuẩn. Có Actionable Insights cho từng nhóm. |
| **[R] Resource** | Đọc Raw Data từ `FACT_INVOICES` + `DIM_CUSTOMERS` trong SQLite. **Không** sửa schema DB. Xử lý 100% trên Pandas in-memory. |
| **[P] People** | Đối tượng: Marketer, Mentor BA — người dùng nghiệp vụ, không phải kỹ sư kỹ thuật. Ngôn ngữ: Tiếng Việt. |
| **[O] Outline** | Thêm Tab 4 vào file `src/03_dashboard.py`. Không xáo trộn 3 Tab ETL cũ. |
| **[L] Locale** | Python 3.11, Streamlit, Plotly. Chạy local: `streamlit run src/03_dashboard.py`. Định dạng tiền VNĐ. |
| **[E] Example** | Lưới 5×5 Heatmap mô phỏng ảnh `docs/rfm_predictive segments.png`. |

---

## II. Các Quyết Định Kỹ Thuật Đã Chốt

### 1. Kiến Trúc Data Loading: In-Memory Pandas ✅

Logic tính RFM sẽ chạy **trực tiếp trên RAM** thông qua thư viện Pandas, KHÔNG lưu kết quả vào Database.

**Lý do lựa chọn:**
- Cho phép Marketing lọc theo bất kỳ khoảng `Date Range` nào → RFM tự động tính lại tức thì.
- Phù hợp với quy mô dữ liệu giả lập hiện tại (< 100K records).
- Code ngắn gọn: `pd.qcut()` xử lý chia 5 nấc Quintile chỉ trong 1 dòng.

```python
# Công thức cốt lõi
rfm['R'] = pd.qcut(rfm['Recency'].rank(method='first'), q=5, labels=[5,4,3,2,1]).astype(int)
rfm['F'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=5, labels=[1,2,3,4,5]).astype(int)
rfm['M'] = pd.qcut(rfm['Monetary'].rank(method='first'), q=5, labels=[1,2,3,4,5]).astype(int)
rfm['FM_Score'] = ((rfm['F'] + rfm['M']) / 2).round().astype(int)
```

### 2. Bố Trí Không Gian: Tab Số 4 Chuyên Biệt ✅

Marketing Dashboard được thiết kế như một **Workspace biệt lập** bên trong cùng ứng dụng Streamlit (Tab 4), hoàn toàn không chứa các thông số kỹ thuật ETL.

```
st.tabs([
    "💎 Tổng quan & DQC",         ← Tab 1: Dành cho Data Engineer
    "📈 Phân tích Bán hàng",       ← Tab 2: Dành cho Sales Manager
    "📦 Đối tượng & Tồn kho",     ← Tab 3: Dành cho Product Manager
    "🎯 Phân khúc RFM (Marketing)" ← Tab 4: Dành riêng cho Marketer
])
```

### 3. Thang Điểm: 5 Cấp (Quintiles) ✅

| Cấp | Ý Nghĩa |
| --- | --- |
| **5** | Top 20% tốt nhất |
| **4** | Khá tốt |
| **3** | Trung bình |
| **2** | Dưới trung bình |
| **1** | Bottom 20% yếu nhất |

> **Lưu ý quan trọng:** Recency chia **nghịch** (R=5 là người mua GẦN ĐÂY nhất — ngày càng nhỏ là càng tốt). Frequency & Monetary chia **xuôi** (càng nhiều càng cao điểm).

---

## III. Thiết Kế UI/UX Tab 4 Phân Tích RFM

```
┌─────────────────────────────────────────────────────────────┐
│  🎯 Phân Khúc Khách Hàng (RFM Predictive Matrix)            │
│  Module dành riêng cho bộ phận Marketing                    │
├─────────────────────────────────────────────────────────────┤
│  [KPI Row] Tổng KH | Champions % | Avg CLV                  │
├──────────────────────────────┬──────────────────────────────┤
│                              │                              │
│  Lưới 5×5 RFM Heatmap        │  Pie Chart                   │
│  (mô phỏng Predictive        │  Tỷ trọng Phân khúc          │
│   Segments Image)            │                              │
│  Trục X: Recency Score       │                              │
│  Trục Y: FM Score            │                              │
│                              │                              │
├──────────────────────────────┴──────────────────────────────┤
│  📋 Dropdown chọn Phân khúc                                  │
│  💡 Insight Kinh Doanh (text giải thích)                    │
│  📊 Data Table: Tên KH | SĐT | R | F | M | Segment          │
│  📥 Nút Export CSV                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## IV. Ma Trận Mapping 11 Nhóm RFM

Dựa theo ảnh chuẩn `docs/rfm_predictive segments.png`:

| R Score | FM Score | Tên Nhóm | Màu Gợi Ý |
| --- | --- | --- | --- |
| 5 | 4–5 | **Champions** | Xanh ngọc |
| 3–4 | 4–5 | **Loyal Customers** | Xám xanh |
| 1–2 | 4–5 | **Can't Lose Them** | Đỏ nhạt |
| 4–5 | 2–3 | **Potential Loyalist** | Xanh lá nhạt |
| 5 | 1 | **Price Sensitive** | Tím nhạt |
| 4–5 | 1–2 | **Recent Users** | Xanh da trời nhạt |
| 3 | 3 | **Needs Attention** | Xám |
| 3 | 1–2 | **About To Sleep** | Xám nhạt |
| 3 | 1 | **Promising** | Nâu nhạt |
| 1–2 | 2–3 | **Hibernating** | Cam nhạt |
| 1–2 | 1 | **Lost** | Xám đậm |

---

## V. Bảng Actionable Insights (Diễn Giải Kinh Doanh)

| Phân Khúc | Đặc Điểm | Hành Động Đề Xuất |
| --- | --- | --- |
| **Champions** | Mua gần đây, thường xuyên, chi nhiều | Tặng quà tri ân, mời vào club VIP, nhờ mua trước sản phẩm mới |
| **Loyal Customers** | Mua thường xuyên, giá trị ổn | Upsell sản phẩm bổ trợ, tích điểm đổi quà |
| **Potential Loyalist** | Mua gần đây, giá trị tốt | Gửi voucher mua lần sau, gợi ý đăng ký membership |
| **Recent Users** | Mới mua lần đầu | Email chào mừng, giới thiệu nhóm hàng bán chạy |
| **Promising** | Mua gần, nhưng ít và thấp | Khuyến khích mua combo để nhận ưu đãi |
| **Needs Attention** | Trung bình mọi mặt | Ưu đãi có thời hạn, tạo cảm giác khan hiếm |
| **About To Sleep** | Đang giảm dần | Gửi "Chúng mình nhớ bạn" + ưu đãi nhỏ |
| **Can't Lose Them** | Từng là VIP, đã lâu vắng | Gọi điện trực tiếp, ưu đãi đặc biệt 30–50% |
| **Hibernating** | Mua ít, lâu rồi không mua | Coupon mạnh để kéo khách về |
| **Lost** | Đã mất hoàn toàn | Thử 1 lần cuối (win-back), nếu không thì bỏ |
| **Price Sensitive** | Chỉ mua lúc Sale | Chỉ thông báo khi có chương trình Sale lớn |

---

## VI. Phạm Vi File Thay Đổi

| Hành Động | File | Ghi Chú |
| --- | --- | --- |
| **[NEW/MODIFY]** | `src/03_dashboard.py` | File dashboard chính Streamlit |
| **[NEW]** | `requirements.txt` | Bổ sung `streamlit`, `plotly` |
| **[UPDATE]** | `docs/dashboard-pipeline-design.md` | Đã cập nhật mô tả Tab 4 ✅ |

---

## VII. Hướng Dẫn Chạy Ứng Dụng (Windows Environment)

```batch
REM B1: Activate virtual environment (Windows)
venv\Scripts\activate

REM B2: Cài đặt dependencies (nếu chưa có)
pip install streamlit plotly pandas

REM B3: Chạy Dashboard từ root project
streamlit run src/03_dashboard.py
```

> **Lưu ý về DB Path:** File `src/03_dashboard.py` mặc định tìm database tại `warehouse/retail_synthetic.db` tính từ **thư mục gốc project** (không phải từ `src/`). Hãy chắc chắn **chạy lệnh `streamlit run` từ root directory** của project (`D:\Workspaces\gjs-smart-retail-code`).

---

## VIII. Verification Checklist

- [ ] `streamlit run src/03_dashboard.py` chạy thành công, không văng lỗi
- [ ] Tab 4 hiển thị đúng tiêu đề "Phân khúc RFM (Marketing)"
- [ ] Lưới Heatmap 5×5 render với data thực từ database
- [ ] Thay đổi Date Range → RFM tính lại in-memory, Heatmap cập nhật
- [ ] Dropdown phân khúc hiển thị đúng 11 nhóm
- [ ] Bảng Data Table lọc đúng danh sách khách theo phân khúc được chọn
- [ ] Nút Export CSV tải được file `.csv` chứa đúng data
- [ ] Không có lỗi `qcut` khi dữ liệu có giá trị trùng (đã có `safe_qcut` fallback)
