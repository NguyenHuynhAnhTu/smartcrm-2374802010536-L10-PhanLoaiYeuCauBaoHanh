# Smart CRM – Tự động phân loại yêu cầu bảo hành

**Sinh viên:** Nguyễn Huỳnh Anh Tú – MSSV: 2374802010536

**Track:** AI

**Học phần:** Chuyên đề Tốt nghiệp 1 

## 1. Mô tả bài toán

Xây dựng hệ thống AI tự động phân loại yêu cầu bảo hành của khách hàng.

Luồng nghiệp vụ:

Khách hàng gửi nội dung yêu cầu bảo hành:
+hệ thống tiếp nhận nội dung
+tiền xử lý văn bản
+mô hình AI phân loại yêu cầu
+trả về nhóm yêu cầu bảo hành tương ứng.

## 2. Phạm vi

### Làm:

-Thu thập và xử lý dữ liệu mô tả yêu cầu bảo hành.
-Tiền xử lý dữ liệu văn bản.
-Phân tích phân bố các nhóm nhãn.
-Xây dựng mô hình phân loại yêu cầu bảo hành.
-Đánh giá mô hình trên tập dữ liệu kiểm thử.
-Đóng gói mô hình để có thể gọi và kiểm thử.

### Không làm:

-Không xây dựng hệ thống CRM hoàn chỉnh.
-Không xử lý toàn bộ quy trình bảo hành thực tế.
-Không thay thế nhân viên xử lý bảo hành.
-Không sử dụng LLM/API bên ngoài để thay thế mô hình phân loại chính.

## 3. Công nghệ sử dụng
Ngôn ngữ: Python 
Xử lý dữ liệu: Pandas, NumPy 
Machine Learning: Scikit-learn 
Tiền xử lý văn bản: TF-IDF 
Mô hình: baseline Logistic Regression 
Môi trường: Python virtual environment (venv) 
Quản lý phiên bản: Git, GitHub 

## 4. Cấu trúc thư mục

smartcrm-2374802010536-L10-PhanLoaiYeuCauBaoHanh/
├── docs/
├── data/
├── notebooks/
├── src/
│   ├── preprocess.py
│   ├── train.py
│   └── predict.py
├── models/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

## 5. Hướng dẫn cài đặt & chạy
Bước 1: Tạo môi trường ảo
"python -m venv .venv"
Bước 2: Kích hoạt môi trường ảo trên Windows
".venv\Scripts\activate"
Bước 3: Cài đặt thư viện
"pip install pandas numpy scikit-learn jupyter python-dotenv"
Bước 4: Kiểm tra môi trường
"python -c "import pandas, sklearn; print('OK', pandas.__version__, sklearn.__version__)""
Bước 5: Chạy chương trình
Sau khi hoàn thiện mã nguồn:
"python src/train.py"