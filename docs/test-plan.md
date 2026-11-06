# Test Plan - Hệ thống Phân loại Sự cố (Track AI)

## 1. Phạm vi kiểm thử
- **Trong phạm vi:** Kiểm thử hàm `clean_text`, `build_features`; kiểm tra rò rỉ dữ liệu (Data Leakage); kiểm tra tính tái lập; kiểm thử API dự đoán với dữ liệu hợp lệ, sai và các giá trị biên.
- **Chủ ý KHÔNG kiểm thử:** Giao diện người dùng (UI/UX) vì không chứa logic phức tạp. Hiệu năng (Performance) vì thuộc môn khác.

## 2. Bốn nguồn sinh Test Case và Kỹ thuật chọn dữ liệu
Hệ thống có 14 test case:
- **Nguồn 1 (Tiêu chí chấp nhận):** TC-01, TC-02, TC-03 (Luồng đúng).
- **Nguồn 2 (Luồng ngoại lệ):** TC-04, TC-05, TC-06 (Dữ liệu rỗng, khoảng trắng, null).
- **Nguồn 3 (Quy tắc nghiệp vụ):** TC-07 (Che SĐT), TC-08 (Rò rỉ), TC-09 (Tái lập), TC-10 (Văn bản dài).
- **Nguồn 4 (Giá trị biên):** TC-11 đến TC-14 (Độ dài 1, 4, 5, 2001 ký tự).
- **Kỹ thuật chọn dữ liệu:** Phân vùng tương đương (hợp lệ/không hợp lệ) và Phân tích giá trị biên (4, 5, 2000, 2001).

## 3. Tiêu chí thành công
- 100% test case PASS (14/14).
- API trả về mã 422 cho dữ liệu sai.
- Chạy huấn luyện 2 lần với `random_state=42` cho ra kết quả giống hệt.

## 4. Môi trường và Dữ liệu thử
- **Môi trường:** Docker Container, Python 3.9, FastAPI.
- **Dữ liệu:** Hard-code trong file `test_ml.py` (JSON payload, Mock DataFrame). Không phụ thuộc file thật trên máy.