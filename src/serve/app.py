import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import numpy as np
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, constr

from src.features.text import clean_text


# ==========================================
# 1. CẤU HÌNH LOGGING VÀ ĐƯỜNG DẪN
# ==========================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smartcrm.api")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "artifacts" / "model_v1.joblib"


# ==========================================
# 2. ĐỊNH NGHĨA SCHEMA KIỂM TRA DỮ LIỆU VÀO
# ==========================================
class PredictionRequest(BaseModel):
    mo_ta: constr(
        strip_whitespace=True,
        min_length=5,
        max_length=2000
    )


# ==========================================
# 3. QUẢN LÝ VÒNG ĐỜI (NẠP MODEL KHI KHỞI ĐỘNG)
# ==========================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        if not MODEL_PATH.is_file():
            raise FileNotFoundError(f"Khong tim thay file mo hinh tai {MODEL_PATH}")

        bundle = joblib.load(MODEL_PATH)

        app.state.vectorizer = bundle["vectorizer"]
        app.state.model = bundle["model"]
        app.state.model_version = "model_v1"
        app.state.selected_model = bundle.get("selected_model", "unknown")

        app.state.confidence_threshold = float(
            os.getenv("CONFIDENCE_THRESHOLD", "0.70")
        )

        if not 0 <= app.state.confidence_threshold <= 1:
            raise ValueError("Nguong tin cay phai tu 0 den 1")

        if not hasattr(app.state.model, "predict_proba"):
            raise ValueError("Mo hinh khong ho tro predict_proba")

        logger.info("Da nap mo hinh thanh cong!")

    except Exception:
        logger.exception("Khong the khoi dong API")
        raise

    yield # API bắt đầu chạy từ đây


# ==========================================
# 4. KHỞI TẠO ỨNG DỤNG FASTAPI
# ==========================================
app = FastAPI(
    title="Smart CRM L10 - Warranty Classification API",
    version="0.2",
    lifespan=lifespan
)


# ==========================================
# 5. CÁC ENDPOINT API (DÀNH CHO HỆ THỐNG GỌI)
# ==========================================
@app.get("/health")
def health_check(request: Request):
    return {
        "status": "healthy",
        "model_version": request.app.state.model_version,
        "selected_model": request.app.state.selected_model
    }


@app.post("/du-doan")
def du_doan(payload: PredictionRequest, request: Request):

    # 1. Chuẩn hóa văn bản
    text = clean_text(payload.mo_ta)

    # 2. Chuyển văn bản thành TF-IDF
    vector = request.app.state.vectorizer.transform([text])

    # 3. Dự đoán xác suất
    model = request.app.state.model
    probabilities = model.predict_proba(vector)[0]
    classes = model.classes_

    # 4. Lấy top 3 nhóm lỗi
    top_indices = np.argsort(probabilities)[::-1][:3]
    top_3 = []
    for index in top_indices:
        top_3.append({
            "nhom_loi": str(classes[index]),
            "do_tin_cay": round(float(probabilities[index]), 4)
        })

    # 5. Xử lý kết quả cao nhất và ngưỡng tin cậy
    best_index = int(top_indices[0])
    predicted_category = str(classes[best_index])
    confidence = float(probabilities[best_index])

    threshold = request.app.state.confidence_threshold
    need_review = confidence < threshold

    return {
        "nhom_loi_du_doan": predicted_category,
        "do_tin_cay": round(confidence, 4),
        "nhom_loi_goi_y": (
            None if need_review else predicted_category
        ),
        "can_nguoi_xem_lai": need_review,
        "nguong_tin_cay": threshold,
        "top_3": top_3,
        "model_version": request.app.state.model_version
    }


# ==========================================
# 6. GIAO DIỆN WEB HTML (DÀNH CHO DEMO TRỰC QUAN)
# ==========================================
@app.get("/", response_class=HTMLResponse)
def giao_dien_demo():
    html_content = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Demo Phân Loại Sự Cố - Smart CRM</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; padding: 40px; }
            .container { max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
            h2 { color: #1a73e8; text-align: center; margin-bottom: 20px; }
            label { font-weight: 600; color: #333; display: block; margin-bottom: 8px;}
            textarea { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 8px; font-size: 15px; height: 120px; margin-bottom: 15px; box-sizing: border-box; font-family: inherit; resize: vertical;}
            textarea:focus { outline: none; border-color: #1a73e8; box-shadow: 0 0 0 2px rgba(26,115,232,0.2); }
            button { width: 100%; padding: 14px; background-color: #1a73e8; color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; font-weight: bold; transition: 0.3s; }
            button:hover { background-color: #1557b0; }
            #result { margin-top: 25px; padding: 20px; background-color: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 8px; display: none; }
            .label-res { font-weight: bold; color: #555; display: inline-block; width: 160px;}
            .value-res { color: #d93025; font-size: 18px; font-weight: bold; }
            .error { color: #d93025; font-weight: bold; text-align: center; }
            .success-title { color: #1e8e3e; font-weight: bold; margin-bottom: 10px; display: block; border-bottom: 1px solid #e0e0e0; padding-bottom: 10px;}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Hệ Thống Phân Loại Yêu Cầu Bảo Hành</h2>
            
            <label for="mo_ta">Nhập mô tả lỗi của khách hàng:</label>
            <textarea id="mo_ta" placeholder="Ví dụ: Điện thoại của tôi bị sọc màn hình xanh và không cảm ứng được..."></textarea>
            
            <button onclick="phanLoai()">Phân Loại Ngay</button>
            
            <div id="result"></div>
        </div>

        <script>
            async function phanLoai() {
                const text = document.getElementById('mo_ta').value;
                const resultDiv = document.getElementById('result');
                
                // Kiểm tra đầu vào cơ bản ở client
                if (!text || text.trim().length < 5) {
                    resultDiv.style.display = 'block';
                    resultDiv.innerHTML = '<span class="error">Lỗi: Vui lòng nhập ít nhất 5 ký tự!</span>';
                    return;
                }

                resultDiv.style.display = 'block';
                resultDiv.innerHTML = '<span style="color: #1a73e8;">Đang phân tích dữ liệu...</span>';

                try {
                    const response = await fetch('/du-doan', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ mo_ta: text })
                    });

                    const data = await response.json();

                    if (response.ok) {
                        // Format lại giao diện kết quả
                        let top3_html = data.top_3.map(item => 
                            `<li>${item.nhom_loi}: <b>${(item.do_tin_cay * 100).toFixed(2)}%</b></li>`
                        ).join('');

                        resultDiv.innerHTML = `
                            <span class="success-title">✅ Phân tích thành công</span>
                            <p><span class="label-res">Nhóm sự cố:</span> <span class="value-res">${data.nhom_loi_du_doan}</span></p>
                            <p><span class="label-res">Độ tin cậy:</span> <b>${(data.do_tin_cay * 100).toFixed(2)}%</b></p>
                            <p><span class="label-res">Cần xem lại:</span> ${data.can_nguoi_xem_lai ? '<span style="color:#d93025">Có (Độ tin cậy thấp)</span>' : '<span style="color:#1e8e3e">Không</span>'}</p>
                            <div style="margin-top:10px;">
                                <span class="label-res" style="vertical-align: top;">Top 3 gợi ý:</span> 
                                <ul style="display:inline-block; margin:0; padding-left:20px;">${top3_html}</ul>
                            </div>
                        `;
                    } else {
                        // Xử lý lỗi 422 từ FastAPI (Pydantic)
                        let errorMsg = 'Dữ liệu không hợp lệ';
                        if (data.detail && data.detail[0] && data.detail[0].msg) {
                            errorMsg = data.detail[0].msg;
                        }
                        resultDiv.innerHTML = `<span class="error">Lỗi (${response.status}): ${errorMsg}</span>`;
                    }
                } catch (error) {
                    resultDiv.innerHTML = '<span class="error">Lỗi kết nối tới Server! Hãy kiểm tra lại Uvicorn.</span>';
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content