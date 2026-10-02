# Đặc tả bài toán ML – L10

## 1. Tên bài toán

Tự động phân loại yêu cầu bảo hành bằng AI.

## 2. Input / Output

- Input: `issue_desc` – mô tả lỗi của khách hàng.
- Output: `issue_category` – nhóm sự cố và độ tin cậy dự đoán.

## 3. Loại bài toán

Phân loại văn bản nhiều lớp (Multi-class Classification).

## 4. Dataset

- Tên: `issue_descriptions.csv`
- Số mẫu: khoảng 4.000 mô tả lỗi đã được gán nhãn.
- Nguồn: dữ liệu mẫu của case study Smart CRM – Mekong Mobile.

## 5. Định nghĩa nhãn

Hệ thống phân loại thành 6 nhóm:

- `MAN_HINH`
- `PIN`
- `SAC`
- `PHAN_MEM`
- `NUOC_VAO`
- `KHAC`

## 6. Mô hình dự kiến

TF-IDF + Logistic Regression.

## 7. Đánh giá

- Macro F1
- Accuracy
- Precision
- Recall
- Confusion Matrix

## 8. Cách sử dụng kết quả

AI chỉ đưa ra đề xuất để nhân viên kiểm tra và xác nhận hoặc điều chỉnh.