# SRS – Tự động phân loại yêu cầu bảo hành bằng AI

## 1. Giới thiệu và phạm vi

Bài toán: Tự động phân loại yêu cầu bảo hành bằng AI.

Luồng nghiệp vụ:
Nhân viên tiếp nhận nhập mô tả lỗi → hệ thống xử lý → AI phân loại nhóm sự cố
→ hiển thị kết quả và độ tin cậy → nhân viên xác nhận/chỉnh sửa → lưu kết quả.

Ngoài phạm vi:
- Không xây dựng toàn bộ hệ thống CRM/bảo hành.
- Không tự động quyết định cuối cùng thay nhân viên.
- Không xây dựng chatbot.
- Không xử lý ảnh/video.
- Không quản lý kho, bán hàng, marketing.

## 2. Các bên liên quan và vai trò 
 Nhân viên tiếp nhận:  Nhập mô tả, xem kết quả AI, xác nhận/chỉnh sửa, lưu, tra cứu 
 Quản lý trung tâm:  Xem thống kê nhóm sự cố 

## 3. Yêu cầu chức năng

### User Story

 US01  Là nhân viên tiếp nhận, tôi muốn nhập mô tả lỗi của khách hàng, để có thông tin cho việc phân loại yêu cầu bảo hành.  MUST 
 US02  Là nhân viên tiếp nhận, tôi muốn nhận đề xuất nhóm sự cố từ AI, để hỗ trợ phân loại nhanh hơn.  MUST 
 US03  Là nhân viên tiếp nhận, tôi muốn xem nhóm sự cố và độ tin cậy, để kiểm tra kết quả trước khi xác nhận.  MUST 
 US04  Là nhân viên tiếp nhận, tôi muốn xác nhận hoặc điều chỉnh kết quả phân loại, để kết quả cuối phù hợp với đánh giá thực tế.  MUST 
 US05  Là nhân viên tiếp nhận, tôi muốn lưu kết quả phân loại vào phiếu bảo hành, để ghi nhận kết quả xử lý.  MUST 
 US06  Là nhân viên tiếp nhận, tôi muốn tra cứu các yêu cầu đã phân loại, để xem lại thông tin khi cần.  SHOULD 
 US07  Là quản lý trung tâm, tôi muốn xem thống kê các nhóm sự cố, để theo dõi phân bố yêu cầu bảo hành.  SHOULD 

### Functional Requirements

 Mã  Yêu cầu 
------
 FR01  Hệ thống cho phép nhập mô tả lỗi. 
 FR02  Hệ thống phân loại mô tả lỗi thành 1 trong 6 nhóm sự cố. 
 FR03  Hệ thống hiển thị nhóm sự cố và độ tin cậy. 
 FR04  Hệ thống cho phép xác nhận hoặc điều chỉnh kết quả. 
 FR05  Hệ thống lưu kết quả phân loại. 
 FR06  Hệ thống cho phép tra cứu yêu cầu đã phân loại. 
 FR07  Hệ thống cho phép quản lý xem thống kê. 

## 4. Yêu cầu phi chức năng

 Mã  Yêu cầu  Ngưỡng 
---------
 NFR01  Thời gian trả kết quả phân loại  ≤ 2 giây/request 
 NFR02  Tỷ lệ xử lý request thành công  ≥ 95% 
 NFR03  Thời gian hiển thị kết quả tra cứu  ≤ 2 giây 

## 5. Ràng buộc và quy tắc nghiệp vụ

- Có 6 nhóm sự cố: MAN_HINH, PIN, SAC, PHAN_MEM, NUOC_VAO, KHAC.
- AI chỉ đề xuất; nhân viên xác nhận kết quả cuối.
- Confidence ≥ 0,70: hiển thị kết quả như đề xuất.
- Confidence < 0,70: không tự điền, nhân viên chọn thủ công.
- Không dùng kết quả AI để tự động từ chối bảo hành hoặc đánh giá nhân viên.

## 6. Bảng truy vết yêu cầu

 FR  US  Use Case  MoSCoW 
------------
 FR01  US01  UC01 – Nhập mô tả yêu cầu bảo hành  MUST 
 FR02  US02  UC02 – Phân loại yêu cầu bằng AI  MUST 
 FR03  US03  UC03 – Xem kết quả và độ tin cậy  MUST 
 FR04  US04  UC04 – Xác nhận / UC05 – Chỉnh sửa  MUST 
 FR05  US05  UC06 – Lưu kết quả phân loại  MUST 
 FR06  US06  UC07 – Tra cứu yêu cầu đã phân loại  SHOULD 
 FR07  US07  UC08 – Xem thống kê nhóm sự cố  SHOULD 