
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import numpy as np
from fastapi import FastAPI, Request
from pydantic import BaseModel, constr

from src.features.text import clean_text


# Cau hinh logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smartcrm.api")

# Duong dan thu muc goc
PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "artifacts" / "model_v1.joblib"


# Kiem tra du lieu dau vao
class PredictionRequest(BaseModel):
    mo_ta: constr(
        strip_whitespace=True,
        min_length=5,
        max_length=2000
    )


# Nap mo hinh khi API khoi dong
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        if not MODEL_PATH.is_file():
            raise FileNotFoundError("Khong tim thay file mo hinh")

        bundle = joblib.load(MODEL_PATH)

        app.state.vectorizer = bundle["vectorizer"]
        app.state.model = bundle["model"]
        app.state.model_version = "model_v1"
        app.state.selected_model = bundle.get(
            "selected_model", "unknown"
        )

        app.state.confidence_threshold = float(
            os.getenv("CONFIDENCE_THRESHOLD", "0.70")
        )

        if not 0 <= app.state.confidence_threshold <= 1:
            raise ValueError("Nguong tin cay phai tu 0 den 1")

        if not hasattr(app.state.model, "predict_proba"):
            raise ValueError("Mo hinh khong ho tro predict_proba")

        logger.info("Da nap mo hinh thanh cong")

    except Exception:
        logger.exception("Khong the khoi dong API")
        raise

    yield


# Tao ung dung FastAPI
app = FastAPI(
    title="Smart CRM L10 - Warranty Classification API",
    version="0.2",
    lifespan=lifespan
)


# Endpoint kiem tra trang thai
@app.get("/health")
def health_check(request: Request):
    return {
        "status": "healthy",
        "model_version": request.app.state.model_version,
        "selected_model": request.app.state.selected_model
    }


# Endpoint phan loai yeu cau bao hanh
@app.post("/du-doan")
def du_doan(payload: PredictionRequest, request: Request):

    # Chuan hoa van ban
    text = clean_text(payload.mo_ta)

    # Chuyen van ban thanh TF-IDF
    vector = request.app.state.vectorizer.transform([text])

    # Du doan xac suat
    model = request.app.state.model
    probabilities = model.predict_proba(vector)[0]
    classes = model.classes_

    # Lay top 3 nhom loi
    top_indices = np.argsort(probabilities)[::-1][:3]

    top_3 = []

    for index in top_indices:
        top_3.append({
            "nhom_loi": str(classes[index]),
            "do_tin_cay": round(float(probabilities[index]), 4)
        })

    # Lay ket qua cao nhat
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
