# Bug Log

## BUG-01: Lỗi thiếu Validation dữ liệu đầu vào API
1. **Mã và mức độ:** BUG-01 - Critical.
2. **Phát hiện bởi:** TC-04 (Kiểm tra API từ chối chuỗi rỗng).
3. **Triệu chứng:** API trả về 200 OK khi gửi chuỗi rỗng, khiến mô hình AI dự đoán sai lệch.
4. **Cách tái lập:** POST /du-doan với body `{"mo_ta": ""}`.
5. **Nguyên nhân:** Xóa mất tham số `min_length=5` trong class `PredictionRequest` tại `app.py`.
6. **Cách sửa:** Khôi phục `min_length=5` trong `src/serve/app.py`.
7. **Link commit và xác nhận:** https://github.com/NguyenHuynhAnhTu/smartcrm-2374802010536-L10-PhanLoaiYeuCauBaoHanh/commit/fb3d2282f4433e0cf2a9ddb777dc056299235ffb - Đã chạy lại TC-04, PASS (trả về 422).

## BUG-02: Lỗi không thể tái lập kết quả huấn luyện
1. **Mã và mức độ:** BUG-02 - Major.
2. **Phát hiện bởi:** TC-09 (Kiểm tra tính tái lập).
3. **Triệu chứng:** Kết quả huấn luyện thay đổi mỗi khi chạy lại script train.
4. **Cách tái lập:** Xóa `random_state` trong hàm chia dữ liệu và khởi tạo mô hình, chạy train 2 lần.
5. **Nguyên nhân:** Thiếu tham số `random_state=42` tại file `train.py`.
6. **Cách sửa:** Thêm lại `random_state=seed` vào `train_test_split` và model trong `src/models/train.py`.
7. **Link commit và xác nhận:** https://github.com/NguyenHuynhAnhTu/smartcrm-2374802010536-L10-PhanLoaiYeuCauBaoHanh/commit/69ac003a9e8f0c216110369aaf3c448b91150fdf - Đã chạy lại TC-09, PASS.

## BUG-03: Lỗi logic làm sạch văn bản
1. **Mã và mức độ:** BUG-03 - Minor.
2. **Phát hiện bởi:** TC-02 (Kiểm tra hàm clean_text giữ dấu tiếng Việt).
3. **Triệu chứng:** Văn bản không được chuyển về chữ thường.
4. **Cách tái lập:** Xóa dòng `text = text.lower()` trong hàm `clean_text` và chạy test TC-02.
5. **Nguyên nhân:** Vô tình làm mất logic chuyển đổi chữ thường trong `text.py`.
6. **Cách sửa:** Khôi phục `text = text.lower()` trong `src/features/text.py`.
7. **Link commit và xác nhận:** https://github.com/NguyenHuynhAnhTu/smartcrm-2374802010536-L10-PhanLoaiYeuCauBaoHanh/commit/52d82d18fa5064db6c8275d71477291d1f983745 - Đã chạy lại TC-02, PASS.