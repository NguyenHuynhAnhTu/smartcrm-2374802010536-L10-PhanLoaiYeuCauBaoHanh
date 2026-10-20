# Nhật ký thay đổi thiết kế

## Sau phản hồi Bài tập 1
**Thời điểm:** Buổi 8 – Ngày 19 tháng 10 năm 2026

### TD-01 – Chuẩn hóa mã Use Case và bảng truy vết yêu cầu

- **Phản hồi của GV:** Sơ đồ Use Case sử dụng mã US-01 đến US-08 thay vì UC01 đến UC08; bảng truy vết liên kết FR05 với US05 không đúng với nội dung User Story; đặc tả UC02 ghi nhầm User Story liên quan; US08 chưa được thể hiện trong bảng truy vết.
- **Quyết định:** SỬA.
- **Lý do:** Cần phân biệt mã User Story (US) và mã Use Case (UC), đồng thời bảo đảm các liên kết giữa yêu cầu chức năng, User Story và Use Case nhất quán trong toàn bộ tài liệu.
- **Ảnh hưởng:** Chuẩn hóa mã Use Case trên sơ đồ; cập nhật bảng truy vết và đặc tả Use Case. Sau khi điều chỉnh danh sách User Story, các mã và liên kết được cập nhật theo thiết kế mới gồm US01–US07 và UC01–UC07.

### TD-02 – Điều chỉnh số lượng User Story

- **Phản hồi của GV:** Thiết kế có 8 User Story, vượt yêu cầu từ 5 đến 7 User Story.
- **Quyết định:** SỬA.
- **Lý do:** Danh sách User Story cần đáp ứng giới hạn của bài tập và tránh tách riêng những thao tác có thể được mô tả trong cùng một mục tiêu nghiệp vụ.
- **Ảnh hưởng:** Gộp User Story xác nhận nhóm sự cố và User Story chỉnh sửa nhóm sự cố thành US04 – Xác nhận hoặc chỉnh sửa kết quả phân loại. Các User Story phía sau được đánh lại mã: US05 – Lưu kết quả phân loại, US06 – Tra cứu yêu cầu đã phân loại và US07 – Xem thống kê nhóm sự cố. Cập nhật SRS, bảng truy vết và sơ đồ liên quan.

### TD-03 – Bổ sung chú thích ký hiệu cho các sơ đồ

- **Phản hồi của GV:** Sơ đồ Use Case, sơ đồ kiến trúc và ML pipeline chưa có chú thích ký hiệu.
- **Quyết định:** SỬA.
- **Lý do:** Chú thích giúp người đọc hiểu ý nghĩa của các thành phần, ký hiệu và mối quan hệ được sử dụng trong từng sơ đồ.
- **Ảnh hưởng:** Bổ sung chú thích tác nhân, Use Case, ranh giới hệ thống và các quan hệ `include`/`extend` trên sơ đồ Use Case; bổ sung chú thích phù hợp cho sơ đồ kiến trúc và ML pipeline. Sử dụng các tệp nguồn có thể chỉnh sửa và cập nhật hình ảnh xuất ra trong thư mục `docs/`.

### TD-04 – Bổ sung tiêu chí định nghĩa sáu nhãn phân loại

- **Phản hồi của GV:** Chưa có định nghĩa rõ ràng cho các nhãn MAN_HINH, PIN, SAC, PHAN_MEM, NUOC_VAO và KHAC.
- **Quyết định:** SỬA.
- **Lý do:** Tiêu chí gán nhãn cụ thể giúp việc phân loại dữ liệu nhất quán hơn, hỗ trợ kiểm tra chất lượng dữ liệu và đánh giá kết quả mô hình.
- **Ảnh hưởng:** Bổ sung mô tả, dấu hiệu nhận biết và ví dụ cho từng nhãn trong `docs/ml-problem-statement.md`. Làm rõ cách phân loại các mô tả mơ hồ hoặc có dấu hiệu thuộc nhiều nhóm; đối chiếu tiêu chí với dữ liệu thực tế trước khi áp dụng.

### TD-05 – Liên kết wireframe với Use Case

- **Phản hồi của GV:** Wireframe chưa ghi rõ mỗi màn hình tương ứng với Use Case nào.
- **Quyết định:** SỬA.
- **Lý do:** Liên kết giữa màn hình và Use Case giúp đối chiếu giao diện với yêu cầu nghiệp vụ, đồng thời kiểm tra tính nhất quán giữa SRS, sơ đồ Use Case và thiết kế giao diện.
- **Ảnh hưởng:** Bổ sung mã Use Case tương ứng cho từng màn hình trong wireframe; đối chiếu lại chức năng của các màn hình với đặc tả Use Case và bảng truy vết yêu cầu.

### TD-06 – Hoàn thiện cấu trúc repo và tài liệu dự án

- **Phản hồi của GV:** Tại thời điểm nộp BT1, repo có một commit và thiếu thư mục `docs/`, các tệp sơ đồ `.drawio` gốc, `srs.md`, `ai-disclosure.md` và `ml-problem-statement.md`.
- **Quyết định:** SỬA.
- **Lý do:** Repo cần lưu trữ đầy đủ tài liệu yêu cầu, thiết kế, tệp nguồn sơ đồ và thông tin sử dụng AI để hỗ trợ kiểm tra, chỉnh sửa và theo dõi tiến độ giữa các bài tập.
- **Ảnh hưởng:** Kiểm tra và hoàn thiện cấu trúc repo; bổ sung hoặc cập nhật các tài liệu còn thiếu; lưu tệp `.drawio` có thể chỉnh sửa bên cạnh hình ảnh xuất ra; cập nhật README và tạo các commit riêng theo từng nhóm công việc bằng thông điệp phù hợp.