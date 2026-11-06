# Bảng khai báo sử dụng công cụ AI (AI Disclosure)

Trong quá trình thực hiện đồ án (Bài tập 1, 2 và 3), em có sử dụng công cụ AI (ChatGPT) để hỗ trợ một số công việc kỹ thuật. Em cam kết mọi kết quả do AI gợi ý đều được em trực tiếp kiểm chứng, chạy thử và điều chỉnh cho phù hợp với dự án thực tế. Dưới đây là bảng khai báo chi tiết:

| STT | Công cụ AI | Nội dung công việc được AI hỗ trợ | Tệp / Hàm / Vị trí liên quan | Cách sinh viên kiểm chứng / Tự đánh giá |
| :--- | :--- | :--- | :--- | :--- |
| 1 | ChatGPT | Gợi ý cách sửa lỗi môi trường (lỗi font tiếng Việt `UnicodeEncodeError` trên Windows). | `src/models/train.py` | Tự thêm `sys.stdout.reconfigure(encoding='utf-8')` vào file và chạy lại script train, kiểm tra thấy không còn văng lỗi. |
| 2 | ChatGPT | Hướng dẫn viết hàm validate dữ liệu đầu vào bằng thư viện Pydantic. | `src/serve/app.py` (`PredictionRequest`) | Tự dùng Postman/Swagger gửi request sai (nhập 1 ký tự), thấy API trả về lỗi 422 đúng như mong đợi. |
| 3 | ChatGPT | Gợi ý cấu trúc và viết các test case bằng Pytest (test API, test rò rỉ dữ liệu, test tái lập). | `src/tests/test_ml.py` | Tự chạy lệnh `pytest src/tests/ -v` trên Terminal. Đảm bảo 14/14 test case đều báo `PASSED`. Tự cố tình sửa code sai để thấy test báo `FAILED`. |
| 4 | ChatGPT | Hướng dẫn cấu hình Docker (viết `Dockerfile` và `docker-compose.yml`). | `Dockerfile`, `docker-compose.yml` | Tự chạy lệnh `docker compose up -d --build` trên máy. Kiểm tra container chạy trạng thái `Up (healthy)` và truy cập được giao diện web. |
| 5 | ChatGPT | Gợi ý nội dung cho các tài liệu hướng dẫn (Test Plan, Bug Log, Model Card). | Thư mục `docs/` | Tự điền thông tin thực tế của dự án vào (số liệu F1, thông tin bug, link commit) và đối chiếu lại với code thực tế. |
| 6 | ChatGPT | Hướng dẫn sửa lỗi đường dẫn (ModuleNotFoundError) khi chạy Uvicorn. | Terminal | Tự chạy lại các lệnh `uvicorn` và kiểm tra thấy server báo `Application startup complete`. |

**Cam kết của sinh viên:**
Em xin cam đoan không sao chép nguyên văn mã nguồn hoặc tài liệu của người khác dưới mọi hình thức. Mọi dòng code trong dự án đều do em trực tiếp gõ, chạy thử, gỡ lỗi và thấu hiểu logic. Các công cụ AI chỉ đóng vai trò như một người hướng dẫn (mentor) gợi ý giải pháp kỹ thuật. 

**Sinh viên thực hiện**
Nguyễn Huỳnh Anh Tú - MSSV: 2374802010536