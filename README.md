Smart CRM – Tự động phân loại yêu cầu bảo hành

Sinh viên: Nguyễn Huỳnh Anh Tú – MSSV: 2374802010536
Track: AI
Học phần: Chuyên đề Tốt nghiệp 1

1. Mô tả bài toán

Xây dựng hệ thống AI hỗ trợ tự động phân loại yêu cầu bảo hành dựa trên mô tả lỗi của khách hàng.

Luồng nghiệp vụ:

Khách hàng cung cấp mô tả lỗi → Hệ thống tiếp nhận nội dung → Tiền xử lý văn bản → Mô hình AI đề xuất nhóm sự cố → Hiển thị kết quả để nhân viên kiểm tra và xác nhận.

Hệ thống sử dụng sáu nhóm sự cố: MAN_HINH, PIN, SAC, PHAN_MEM, NUOC_VAO và KHAC.

2. Yêu cầu môi trường

Hệ điều hành: Windows 10/11.

Ngôn ngữ: Python; phiên bản cụ thể cần được ghi theo kết quả kiểm tra môi trường thực tế.

Thư viện xử lý dữ liệu: Pandas, NumPy.

Thư viện học máy: Scikit-learn.

Thư viện trực quan hóa và phân tích dữ liệu: Matplotlib, Jupyter Notebook.

Dữ liệu đầu vào: data/issue_descriptions.csv.

Quản lý mã nguồn: Git và GitHub.

Các phiên bản Python và thư viện được kiểm tra, thống nhất và ghi trong requirements.txt trước khi hoàn thiện hướng dẫn cài đặt.

3. Phạm vi

Trong phạm vi

Đọc và kiểm tra dữ liệu mô tả yêu cầu bảo hành.

Tiền xử lý văn bản.

Phân tích phân bố các nhóm nhãn.

Xây dựng và đánh giá mô hình phân loại.

Hiển thị nhóm sự cố được đề xuất để nhân viên kiểm tra.

Ngoài phạm vi

Không xây dựng toàn bộ hệ thống CRM.

Không xử lý toàn bộ quy trình bảo hành thực tế.

Không tự động thay thế quyết định cuối cùng của nhân viên.

Không xử lý ảnh/video.

Không sử dụng LLM/API bên ngoài để thay thế mô hình phân loại chính.

4. Công nghệ sử dụng

Python.

Pandas, NumPy.

Scikit-learn.

TF-IDF để trích xuất đặc trưng văn bản.

Logistic Regression làm một mô hình phân loại cần đánh giá.

Matplotlib và Jupyter Notebook phục vụ phân tích dữ liệu.

Git và GitHub để quản lý mã nguồn.

5. Cấu trúc dự án, cài đặt và chạy

5.1. Cấu trúc thư mục

smartcrm-2374802010536-L10-PhanLoaiYeuCauBaoHanh/
├── data/
│   └── issue_descriptions.csv
├── docs/
│   ├── srs.md
│   ├── ml-problem-statement.md
│   ├── architecture.drawio.png
│   ├── ML_pipiline.png
│   ├── UseCaseDiagram.drawio
│   └── UseCaseDiagram.png
├── models/
├── notebooks/
├── src/
│   ├── data/
│   │   └── load.py
│   ├── features/
│   └── models/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── thay-doi-thiet-ke.md

5.2. Cài đặt môi trường

Mở PowerShell tại thư mục gốc của dự án và chạy:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pandas numpy scikit-learn matplotlib jupyter

Sau khi kiểm tra phiên bản thư viện thực tế, cập nhật và khóa các phiên bản tương ứng trong requirements.txt.

5.3. Chạy module nạp dữ liệu

Khi đã cài đủ thư viện trong đúng môi trường Python, chạy:

python -m src.data.load

Module đọc dữ liệu từ data/issue_descriptions.csv và hiển thị kích thước dữ liệu, tên cột, số ô trống, phân bố nhãn và một số dòng dữ liệu mẫu.

6. Trạng thái hiện tại – Buổi 8

Đã thực hiện

Tạo cấu trúc thư mục ban đầu gồm src/data/, src/features/, src/models/ và notebooks/.

Đọc được data/issue_descriptions.csv bằng Pandas trong lệnh kiểm tra dữ liệu.

Kiểm tra dataset có 2.400 dòng và 4 cột.

Kiểm tra không có ô trống trong bốn cột.

Thống kê phân bố của sáu nhãn phân loại.

Đang hoàn thiện

Xác nhận module src/data/load.py chạy thành công trong môi trường Python đã thống nhất.

Hoàn thiện notebook EDA với thống kê độ dài văn bản và biểu đồ phân bố nhãn.

Viết nhận xét về mất cân bằng lớp và kiểm tra các trường hợp có khả năng nhiễu nhãn.

Kiểm tra ảnh minh chứng trong docs/ thể hiện kết quả chạy thành công.

Cập nhật README và các tài liệu liên quan theo kết quả thực tế.

Ghi chú: Buổi 8 tập trung vào việc xây dựng cấu trúc dự án, nạp dữ liệu và phân tích dữ liệu ban đầu. Việc huấn luyện, so sánh và đánh giá mô hình được thực hiện ở các bước phát triển tiếp theo.