# Smart CRM – Tự động phân loại yêu cầu bảo hành

**Sinh viên:** Nguyễn Huỳnh Anh Tú – MSSV: 2374802010536  
**Track:** AI  
**Học phần:** Chuyên đề Tốt nghiệp 1
**Link repo Github:**`https://github.com/NguyenHuynhAnhTu/smartcrm-2374802010536-L10-PhanLoaiYeuCauBaoHanh`
**Tag phiên bản:** `v0.2`
## 1. Mô tả bài toán

Xây dựng hệ thống AI hỗ trợ phân loại yêu cầu bảo hành dựa trên mô tả lỗi của khách hàng.

Luồng xử lý chính:
Khách hàng cung cấp mô tả lỗi → Nạp dữ liệu → Tiền xử lý văn bản → Trích xuất đặc trưng TF-IDF → Mô hình phân loại → Đánh giá kết quả → Triển khai API (FastAPI).

Hệ thống phân loại yêu cầu bảo hành thành sáu nhóm:
- `MAN_HINH`: Lỗi màn hình.
- `PIN`: Lỗi pin.
- `SAC`: Lỗi sạc.
- `PHAN_MEM`: Lỗi phần mềm.
- `NUOC_VAO`: Lỗi do nước vào.
- `KHAC`: Các lỗi khác chưa thuộc năm nhóm trên.

Mô hình có vai trò hỗ trợ đề xuất nhóm sự cố. Việc xác nhận kết quả cuối cùng thuộc về nhân viên.

## 2. Yêu cầu môi trường

- Hệ điều hành: Windows 10/11, macOS, Linux.
- Python: 3.9+.
- Bộ dữ liệu: `data/issue_descriptions.csv`.
- Thư viện: Pandas, NumPy, Scikit-learn, Joblib, FastAPI, Uvicorn, Pytest, v.v.
- Quản lý mã nguồn: Git và GitHub.

Các phiên bản thư viện được ghim trong `requirements.txt`.

## 3. Cài đặt và chạy dự án

### 3.1. Cấu trúc thư mục

text
smartcrm-2374802010536-L10-PhanLoaiYeuCauBaoHanh/  # Thư mục gốc của toàn bộ dự án
│
├── configs/                  # THƯ MỤC CẤU HÌNH (Configuration)
│   └── train.yaml            # Chứa các siêu tham số (hyperparameters), đường dẫn dữ liệu. Giúp thay đổi thí nghiệm mà không cần sửa code.
│
├── data/                     # THƯ MỤC DỮ LIỆU (Data)
│   └── issue_descriptions.csv# Tập dữ liệu thô chứa 2400 mẫu mô tả lỗi của khách hàng.
│
├── docs/                     # THƯ MỤC TÀI LIỆU (Documentation)
│                             # Chứa các file báo cáo PDF, hình ảnh minh chứng, sơ đồ kiến trúc, file thiết kế (srs.md, ml-problem-statement.md).
│
├── reports/                  # THƯ MỤC BÁO CÁO KẾT QUẢ (Reports)
│   └── metrics.json          # File JSON lưu trữ các chỉ số đánh giá mô hình (Accuracy, F1-score, Confusion Matrix). Dùng để chèn số liệu vào báo cáo.
│
├── src/                      # THƯ MỤC MÃ NGUỒN CHÍNH (Source Code)
│   │
│   ├── data/                 # Lớp xử lý dữ liệu
│   │   └── load.py           # Code thực hiện việc đọc file CSV và kiểm tra tính hợp lệ của dữ liệu đầu vào.
│   │
│   ├── features/             # Lớp trích xuất đặc trưng
│   │   └── text.py           # Chứa hàm clean_text() để làm sạch văn bản (xóa ký tự đặc biệt, đưa về chữ thường).
│   │
│   ├── models/               # Lớp huấn luyện mô hình
│   │   └── train.py          # Code huấn luyện, so sánh các mô hình (Dummy, Logistic, ComplementNB), chia tập dữ liệu và lưu mô hình tốt nhất.
│   │
│   ├── serve/                # Lớp triển khai (Serving/Deployment)
│   │   └── app.py            # Code xây dựng API bằng FastAPI. Chứa giao diện web HTML và các endpoint (/du-doan, /health) để mô hình AI có thể giao tiếp với bên ngoài.
│   │
│   └── tests/                # THƯ MỤC KIỂM THỬ (Testing)
│       ├── test_text.py      # Unit test kiểm tra xem hàm làm sạch văn bản có hoạt động đúng không.
│       └── test_api.py       # Unit test kiểm tra API (gửi câu đúng, câu sai, kiểm tra trạng thái hệ thống).
│
├── artifacts/                # THƯ MỤC LƯU TRỮ MÔ HÌNH (Artifacts)
│   └── model_v1.joblib       # File nhị phân chứa mô hình và vectorizer đã được huấn luyện xong. (Thư mục này bị chặn bởi .gitignore, không đẩy lên Git).
│
├── .env.example              # File mẫu chứa danh sách các biến môi trường (Ví dụ: CONFIDENCE_THRESHOLD=0.70). Không chứa dữ liệu thật.
├── .gitignore                # File cấu hình Git: Chặn các file rác, file mô hình nặng, file bảo mật (.env) không cho đẩy lên GitHub.
├── requirements.txt          # Danh sách các thư viện cần thiết (đã ghim phiên bản bằng dấu ==) để cài đặt môi trường.
└── README.md                 # File hướng dẫn "sống còn": Cách cài đặt, cách chạy test, cách chạy API và khởi động server.

### 3.2. Tạo môi trường Python
Mở Terminal (PowerShell/CMD) tại thư mục gốc của dự án và thực hiện:

bash
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

### 3.3. Chạy Unit Test
Hệ thống có 9 bài kiểm thử (bao gồm test tiền xử lý văn bản và test API). Chạy lệnh sau để kiểm tra:

bash
python -m pytest src/tests/ -v
(Kết quả kỳ vọng: 9 passed).

### 3.4. Huấn luyện và đánh giá mô hình (Nếu cần tạo lại Model)
bash
python -m src.models.train --config configs/train.yaml
Quy trình này sẽ tạo ra:

reports/metrics.json: Lưu metric và các kết luận đánh giá.

artifacts/model_v1.joblib: Lưu model cùng vectorizer.

### 3.5. Khởi chạy API và Giao diện Web Demo
Để khởi chạy server, chạy lệnh sau:

bash
uvicorn src.serve.app:app --reload
Sau khi server báo Uvicorn running on http://127.0.0.1:8000:

Truy cập http://127.0.0.1:8000/ để mở giao diện nhập liệu trực quan.

Truy cập http://127.0.0.1:8000/docs để xem tài liệu Swagger UI của API.

Truy cập http://127.0.0.1:8000/health để kiểm tra trạng thái hệ thống.

## 4. Kết quả thực nghiệm AI
Bộ dữ liệu có 2.400 mẫu, thuộc sáu nhóm sự cố. Dữ liệu được chia theo tỷ lệ 70% train, 15% validation và 15% test.

Kết quả của lần chạy thực nghiệm:

Mô hình	Accuracy validation	Macro F1 validation
DummyClassifier	0.2139	0.0587
Logistic Regression	0.8083	0.8008
ComplementNB	0.8333	0.8236
ComplementNB được chọn dựa trên Macro F1 của validation.

Kết quả test của mô hình được chọn:

Accuracy: 0.8389.

Macro F1: 0.8318.

Ba nhận xét từ confusion matrix:

Cặp PIN và SAC dễ bị nhầm lẫn nhất (17 dự đoán nhầm). Cần kiểm tra lại định nghĩa nhãn.

PHAN_MEM có Recall thấp nhất (0.6667). Mô hình nhận diện đúng 38/57 mẫu.

MAN_HINH nhận nhiều dự đoán dương tính giả nhất. Cần kiểm tra thêm.

Chi tiết kết quả được lưu trong reports/metrics.json.