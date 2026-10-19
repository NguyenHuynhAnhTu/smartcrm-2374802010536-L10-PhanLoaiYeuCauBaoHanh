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

- `MAN_HINH`: lỗi màn hình
Định nghĩa: Mô tả có dấu hiệu trực tiếp liên quan đến màn hình hiển thị hoặc chức năng cảm ứng của thiết bị. 
Ví dụ: Bị nứt vỡ, sọc màn loang màu, không phản hồi cảm ứng,... 
- `PIN`: Lỗi pin
Định nghĩa: Mô tả cho thấy pin hoặc khả năng lưu trữ năng lượng của thiết bị hoạt động bất thường.
Ví dụ: pin tụt nhanh, pin bị phồng,...
- `SAC`: Lỗi sạc
Định nghĩa: Mô tả liên quan đến việc tiếp nhận điện năng hoặc quá trình sạc thiết bị.
Ví dụ: thiết bị không nhận sạc, cổng sạc lỏng hoặc hư hỏng, dây cáp hoặc bộ sạc bị hư hỏng,...
- `PHAN_MEM`: Lỗi phần mềm
Định nghĩa: Mô tả cho thấy vấn đề phát sinh từ hệ điều hành, ứng dụng hoặc quá trình xử lý phần mềm của thiết bị, không có bằng chứng rõ ràng về nguyên nhân hư hỏng vật lý.Ví dụ: Thiết bị bị treo hoặc đơ do vấn đề phần mềm được mô tả rõ, ứng dụng thường xuyên bị văng hoặc không mở được,...
- `NUOC_VAO`: Sự cố do nước hoặc chất lỏng xâm nhập
Định nghĩa: Mô tả xác định thiết bị đã tiếp xúc với nước hoặc chất lỏng xâm nhập vào bên trong, hoặc có dấu hiệu hư hỏng được liên hệ trực tiếp với sự cố này.
Ví dụ: thiết bị bị rơi xuống nước hoặc bị chất lỏng đổ vào, người dùng mô tả nước đã lọt vào bên trong thiết bị,Người dùng mô tả nước đã lọt vào bên trong thiết bị,... 
- `KHAC`: Các sự cố khác
Định nghĩa: Mô tả thuộc loại sự cố khác ngoài năm nhóm trên hoặc không cung cấp đủ dấu hiệu để xác định một trong năm nhóm một cách đáng tin cậy.
Ví dụ: Lỗi camera, loa, micro, nút bấm hoặc kết nối mạng mà không có dấu hiệu thuộc các nhóm khác,...

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