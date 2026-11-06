# Model Card - Phân loại Sự cố Bảo hành

## 1. Tổng quan
- **Mô hình:** Complement Naive Bayes (Scikit-learn).
- **Đầu vào:** Văn bản mô tả lỗi.
- **Đầu ra:** 6 nhãn (MAN_HINH, PIN, SAC, PHAN_MEM, NUOC_VAO, KHAC).

## 2. Mục đích sử dụng
Hỗ trợ nhân viên tiếp nhận gợi ý nhóm sự cố. Không dùng để tự động từ chối bảo hành.

## 3. Chỉ số hiệu suất
- Test Accuracy: 0.8389.
- Test Macro F1: 0.8318.
- Sử dụng ngưỡng tin cậy 0.70: Nếu dự đoán < 0.70, gắn cờ `can_nguoi_xem_lai = true`.

## 4. Hạn chế
- Nhầm lẫn giữa PIN và SAC do từ vựng tương tự.
- Nhãn NUOC_VAO có Recall thấp (rủi ro bỏ sót).
- Xử lý kém với văn bản quá ngắn (< 5 từ).