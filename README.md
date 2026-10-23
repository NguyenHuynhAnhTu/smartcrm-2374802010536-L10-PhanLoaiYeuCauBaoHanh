# Smart CRM – Tự động phân loại yêu cầu bảo hành

**Sinh viên:** Nguyễn Huỳnh Anh Tú – MSSV: 2374802010536  
**Track:** AI  
**Học phần:** Chuyên đề Tốt nghiệp 1

## 1. Mô tả bài toán

Xây dựng hệ thống AI hỗ trợ phân loại yêu cầu bảo hành dựa trên mô tả lỗi của khách hàng.

Luồng xử lý chính:

Khách hàng cung cấp mô tả lỗi → Nạp dữ liệu → Tiền xử lý văn bản → Trích xuất đặc trưng TF-IDF → Mô hình phân loại → Đánh giá kết quả.

Hệ thống phân loại yêu cầu bảo hành thành sáu nhóm:

- `MAN_HINH`: Lỗi màn hình.
- `PIN`: Lỗi pin.
- `SAC`: Lỗi sạc.
- `PHAN_MEM`: Lỗi phần mềm.
- `NUOC_VAO`: Lỗi do nước vào.
- `KHAC`: Các lỗi khác chưa thuộc năm nhóm trên.

Mô hình có vai trò hỗ trợ đề xuất nhóm sự cố. Việc xác nhận kết quả cuối cùng thuộc về nhân viên.

## 2. Yêu cầu môi trường

- Hệ điều hành: Windows 10/11.
- Python: 3.9.5.
- Bộ dữ liệu: `data/issue_descriptions.csv`.
- Thư viện: Pandas, NumPy, Scikit-learn, Joblib, Matplotlib, PyYAML và Pytest.
- Quản lý mã nguồn: Git và GitHub.

Các phiên bản thư viện được ghim trong `requirements.txt`.

## 3. Phạm vi

### Trong phạm vi

- Nạp và kiểm tra bộ dữ liệu mô tả lỗi bảo hành.
- Tiền xử lý văn bản tiếng Việt.
- Phân tích phân bố các nhóm nhãn.
- Huấn luyện và so sánh các mô hình phân loại.
- Đánh giá bằng Accuracy, Macro F1, F1 từng lớp và confusion matrix.
- Lưu kết quả đánh giá để phục vụ báo cáo.

### Ngoài phạm vi

- Xây dựng toàn bộ hệ thống CRM.
- Xử lý toàn bộ quy trình bảo hành thực tế.
- Tự động thay thế quyết định cuối cùng của nhân viên.
- Phân loại ảnh hoặc video.
- Sử dụng API bên ngoài để thay thế mô hình phân loại chính.

## 4. Công nghệ sử dụng

- Python.
- Pandas và NumPy để xử lý dữ liệu.
- Scikit-learn để xây dựng mô hình học máy.
- TF-IDF để trích xuất đặc trưng văn bản.
- DummyClassifier làm baseline.
- Logistic Regression và ComplementNB để so sánh mô hình.
- Joblib để lưu mô hình và vectorizer.
- Pytest để kiểm thử.
- Git và GitHub để quản lý mã nguồn.

## 5. Cài đặt và chạy dự án

### 5.1. Cấu trúc thư mục

```text
smartcrm-2374802010536-L10-PhanLoaiYeuCauBaoHanh/
├── configs/
│   └── train.yaml
├── data/
│   └── issue_descriptions.csv
├── docs/
├── reports/
│   └── metrics.json
├── src/
│   ├── data/
│   │   └── load.py
│   ├── features/
│   │   └── text.py
│   ├── models/
│   │   └── train.py
│   └── tests/
│       └── test_text.py
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── thay-doi-thiet-ke.md
```

File `artifacts/model_v1.joblib` được tạo khi chạy quy trình huấn luyện. File này không được đưa vào Git vì đã được cấu hình trong `.gitignore`.

### 5.2. Tạo môi trường Python

Mở PowerShell tại thư mục gốc của dự án và thực hiện từng lệnh:

```powershell
python --version
```

```powershell
python -m venv .venv
```

```powershell
.\.venv\Scripts\Activate.ps1
```

```powershell
python -m pip install --upgrade pip
```

```powershell
python -m pip install -r requirements.txt
```

Kiểm tra các thư viện chính:

```powershell
python -c "import pandas, numpy, sklearn, joblib, matplotlib, yaml, pytest; print('IMPORT OK')"
```

### 5.3. Nạp dữ liệu

```powershell
python -m src.data.load
```

Module nạp dữ liệu đọc tệp `data/issue_descriptions.csv` và hiển thị thông tin kiểm tra dữ liệu.

### 5.4. Chạy unit test

```powershell
python -m pytest -q
```

Lệnh này chạy các unit test trong dự án. Số lượng test PASS cần được cập nhật theo kết quả chạy thực tế.

### 5.5. Huấn luyện và đánh giá mô hình

```powershell
python -m src.models.train --config configs/train.yaml
```

Quy trình huấn luyện sử dụng cấu hình trong `configs/train.yaml`, so sánh mô hình trên tập validation, chọn mô hình theo Macro F1 và tạo các kết quả đầu ra:

- `reports/metrics.json`: Lưu metric và các kết luận đánh giá.
- `artifacts/model_v1.joblib`: Lưu model cùng vectorizer.

**Lưu ý:** Script hiện tại thực hiện cả đánh giá trên tập test. Chỉ chạy quy trình đầy đủ khi thực sự cần tái tạo thí nghiệm; không chạy lại chỉ để kiểm tra README hoặc thay đổi những phần không ảnh hưởng đến mô hình.

## 6. Kết quả thực nghiệm AI

Bộ dữ liệu có 2.400 mẫu, thuộc sáu nhóm sự cố. Dữ liệu được chia theo tỷ lệ 70% train, 15% validation và 15% test.

Kết quả của lần chạy thực nghiệm đã ghi nhận:

| Mô hình | Accuracy validation | Macro F1 validation |
|---|---:|---:|
| DummyClassifier | 0.2139 | 0.0587 |
| Logistic Regression | 0.8083 | 0.8008 |
| ComplementNB | 0.8333 | 0.8236 |

ComplementNB được chọn dựa trên Macro F1 của validation.

Kết quả test của mô hình được chọn:

- Accuracy: **0.8389**.
- Macro F1: **0.8318**.

Ba nhận xét từ confusion matrix:

1. Cặp PIN và SAC dễ bị nhầm lẫn nhất, với tổng cộng 17 dự đoán nhầm theo hai chiều. Cần kiểm tra lại định nghĩa nhãn và các mô tả lỗi có nội dung tương tự.
2. PHAN_MEM có Recall thấp nhất, đạt 0.6667. Mô hình nhận diện đúng 38 trên 57 mẫu PHAN_MEM của tập test.
3. MAN_HINH nhận nhiều dự đoán dương tính giả nhất trong kết quả hiện tại. Đây là dấu hiệu cần kiểm tra thêm, chưa đủ cơ sở để kết luận nhãn này là nhãn thùng rác.

Chi tiết kết quả và confusion matrix được lưu trong `reports/metrics.json`.

## 7. Kiểm thử và trạng thái phát triển

- Module tiền xử lý văn bản nằm tại `src/features/text.py`.
- Unit test tiền xử lý văn bản nằm tại `src/tests/test_text.py`.
- Cấu hình huấn luyện nằm tại `configs/train.yaml`.
- Module nạp dữ liệu nằm tại `src/data/load.py`.
- Module huấn luyện và đánh giá nằm tại `src/models/train.py`.
- Kết quả đánh giá được lưu tại `reports/metrics.json`.

Các công việc tiếp theo gồm hoàn thiện kiểm thử, bổ sung ảnh minh chứng trong `docs/`, kiểm tra hướng dẫn bằng cách clone repo vào thư mục mới và xác nhận luồng chính chạy thành công theo README.