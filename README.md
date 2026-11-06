# Smart CRM – Tự động phân loại yêu cầu bảo hành

**Sinh viên:** Nguyễn Huỳnh Anh Tú – MSSV: 2374802010536  
**Track:** AI  
**Học phần:** Chuyên đề Tốt nghiệp 1  
**Link repo Github:** [smartcrm-2374802010536-L10-PhanLoaiYeuCauBaoHanh](https://github.com/NguyenHuynhAnhTu/smartcrm-2374802010536-L10-PhanLoaiYeuCauBaoHanh)  
**Tag phiên bản:** `v1.0` (Dành cho Bài tập 3)

## 1. Mô tả bài toán

Xây dựng hệ thống AI hỗ trợ phân loại yêu cầu bảo hành dựa trên mô tả lỗi của khách hàng. Hệ thống phân loại yêu cầu thành sáu nhóm: MAN_HINH, PIN, SAC, PHAN_MEM, NUOC_VAO, và KHAC. Mô hình có vai trò hỗ trợ đề xuất nhóm sự cố, việc xác nhận kết quả cuối cùng thuộc về nhân viên.

## 2. Yêu cầu môi trường

- Hệ điều hành: Windows 10/11, macOS, Linux.
- Python: 3.9+.
- Docker Desktop (để chạy hệ thống qua Docker).
- Bộ dữ liệu: `data/issue_descriptions.csv`.

## 3. Cấu trúc thư mục

```text
smartcrm-2374802010536-L10-PhanLoaiYeuCauBaoHanh/
├── .github/workflows/        # Chứa file ci.yml cấu hình GitHub Actions
├── artifacts/                # Nơi lưu model_v1.joblib (bị chặn bởi .gitignore)
├── configs/                  # Chứa file cấu hình train.yaml
├── data/                     # Chứa file dữ liệu issue_descriptions.csv
├── docs/                     # Chứa các tài liệu kỹ thuật (Test plan, Bug log, Model card, v.v.)
├── reports/                  # Chứa file metrics.json
├── src/                      # Mã nguồn chính
│   ├── features/             # Hàm clean_text và build_features
│   ├── models/               # Script huấn luyện train.py
│   ├── serve/                # API FastAPI (app.py)
│   └── tests/                # Các file test (test_ml.py, test_text.py)
├── .env.example              # File mẫu biến môi trường
├── Dockerfile                # File cấu hình Docker
├── docker-compose.yml        # File cấu hình Docker Compose
├── requirements.txt          # Danh sách thư viện
└── README.md                 # File hướng dẫn này
```

## 4. Hướng dẫn chạy Unit Test  
Hệ thống có 14 test case tự động bao phủ đủ 5 loại test (luồng đúng, biên, dữ liệu sai, rò rỉ dữ liệu, tái lập).

bash
python -m pytest src/tests/ -v
(Kết quả kỳ vọng: 14 passed).

## 5. Hướng dẫn chạy dự án bằng Docker 
Hệ thống đã được đóng gói bằng Docker. Do các lý do bảo mật và giới hạn dung lượng, các file cấu hình (.env) và file mô hình (*.joblib) không được đẩy lên Git. Hãy làm đúng theo các bước sau để chạy hệ thống từ thư mục trống:

Bước 1: Cài đặt thư viện và tạo file cấu hình

bash
# Cài đặt các thư viện cần thiết (bao gồm cả pytest)
pip install -r requirements.txt

# Tạo file môi trường từ file mẫu
# Windows:
copy .env.example .env
# Mac/Linux:
# cp .env.example .env
Bước 2: Huấn luyện mô hình (Nếu chưa có file model_v1.joblib)

bash
python -m src.models.train
(Lệnh này sẽ mất khoảng 1-2 phút và tạo ra file artifacts/model_v1.joblib)

Bước 3: Khởi chạy hệ thống bằng Docker

bash
docker compose up -d --build
Bước 4: Kiểm tra hệ thống
Truy cập http://127.0.0.1:8000/ để mở giao diện Web nhập liệu.
Truy cập http://127.0.0.1:8000/docs để xem tài liệu Swagger UI.
Truy cập http://127.0.0.1:8000/health để kiểm tra trạng thái API (kỳ vọng: {"status": "healthy"}).

Để tắt hệ thống, chạy lệnh: docker compose down

## 6. Kết quả thực nghiệm AI
Bộ dữ liệu: 2.400 mẫu, chia tỷ lệ 70% Train / 15% Validation / 15% Test.

Mô hình được chọn: Complement Naive Bayes (dựa trên Macro F1 của validation).

Kết quả Test: Accuracy = 0.8389; Macro F1 = 0.8318.

Chi tiết kết quả và Confusion Matrix được lưu trong reports/metrics.json.

## 7. Tài liệu kỹ thuật (Dành cho Bài tập 3)
Toàn bộ tài liệu kiểm thử và đánh giá được lưu trữ trong thư mục docs/:

Test Plan

Test Report

Bug Log

Deployment Guide

Model Card

AI Disclosure

## 8. Trạng thái CI (Continuous Integration)
Dự án đã được cấu hình GitHub Actions để tự động chạy toàn bộ test mỗi khi có code mới được push lên nhánh main.
https://github.com/NguyenHuynhAnhTu/smartcrm-2374802010536-L10-PhanLoaiYeuCauBaoHanh/actions
