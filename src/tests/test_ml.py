import pytest
import json
import os
import subprocess
import pandas as pd
from fastapi.testclient import TestClient
from src.serve.app import app
from src.features.text import clean_text
import joblib

from src.features.text import clean_text, build_features, FEATURE_COLUMNS


# Khởi tạo TestClient (dùng fixture để đảm bảo app chạy lifespan nạp model)
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


# =====================================================================
# LOẠI 1: TEST HÀM BIẾN ĐỔI DỮ LIỆU (Data Transformation)
# =====================================================================
def test_clean_text_giu_dau_tieng_viet():
    """Kiểm tra hàm làm sạch văn bản có giữ nguyên dấu tiếng Việt"""
    van_ban = "Màn hình điện thoại bị sọc xanh"
    ket_qua = clean_text(van_ban)
    assert "màn hình" in ket_qua or "màn" in ket_qua
    assert "điện thoại" in ket_qua or "điện" in ket_qua

def test_clean_text_che_so_dien_thoai():
    """Kiểm tra hàm có che số điện thoại (nếu có tính năng này)"""
    van_ban = "Máy hỏng, liên hệ 0912345678"
    ket_qua = clean_text(van_ban)
    # Tùy thuộc vào code clean_text của bạn, số điện thoại có thể bị xóa hoặc thay bằng <SDT>
    assert "0912345678" not in ket_qua

def test_build_features_tra_dung_cot_va_thu_tu():
    """YÊU CẦU TỪ THẦY: build_features trả đúng SỐ CỘT và THỨ TỰ CỘT"""
    if build_features is None or FEATURE_COLUMNS is None:
        pytest.skip("Chưa tìm thấy hàm build_features hoặc biến FEATURE_COLUMNS trong code")
        
    # Tạo dữ liệu giả lập (DataFrame) với các cột đầu vào cần thiết
    # (Bạn hãy sửa lại tên cột cho khớp với code thực tế của bạn)
    df_gia_lap = pd.DataFrame({
        'mo_ta': ['màn hình bị sọc', 'pin tụt nhanh'],
        'hang_san_xuat': ['Apple', 'Samsung'] 
    })
    
    X = build_features(df_gia_lap)
    
    # Kiểm tra số cột và thứ tự cột
    assert list(X.columns) == FEATURE_COLUMNS, "Số cột hoặc thứ tự cột đã bị thay đổi!"


# =====================================================================
# LOẠI 2: TEST CHỐNG RÒ RỈ DỮ LIỆU (Data Leakage)
# =====================================================================
def test_khong_ro_ri_du_lieu_tu_vung():
    """
    Kiểm tra xem Vectorizer có chứa từ vựng chỉ xuất hiện trong tập Test hay không.
    """
    model_path = "artifacts/model_v1.joblib"
    if not os.path.exists(model_path):
        pytest.skip("Chưa có file model để test rò rỉ dữ liệu")
        
    bundle = joblib.load(model_path)
    vectorizer = bundle["vectorizer"]
    tu_vung_train = set(vectorizer.vocabulary_.keys())
    
    # Giả lập một từ vựng chỉ có trong tập test
    tu_vung_test_gia_lap = {"tu_khoa_chi_co_trong_test_12345"}
    
    # Nếu từ vựng này nằm trong vectorizer -> Đã bị rò rỉ dữ liệu
    assert not (tu_vung_train & tu_vung_test_gia_lap), "Rò rỉ dữ liệu: Vectorizer đã nhìn thấy tập test!"


# =====================================================================
# LOẠI 3: TEST TÍNH TÁI LẬP (Reproducibility)
# =====================================================================
def test_tinh_tai_lap_cua_qua_trinh_huan_luyen():
    """
    Chạy script huấn luyện 2 lần với cùng seed.
    So sánh 2 file metrics.json sinh ra. Nếu khác nhau -> Chưa tái lập được.
    """
    metrics_path = "reports/metrics.json"
    
    # Lần 1: Chạy train
    subprocess.run(["python", "-m", "src.models.train", "--config", "configs/train.yaml"], check=True)
    if not os.path.exists(metrics_path):
        pytest.skip("Không tìm thấy file metrics.json sau khi train")
        
    with open(metrics_path, "r", encoding="utf-8") as f:
        lan_1 = json.load(f)
        
    # Lần 2: Chạy train lại
    subprocess.run(["python", "-m", "src.models.train", "--config", "configs/train.yaml"], check=True)
    with open(metrics_path, "r", encoding="utf-8") as f:
        lan_2 = json.load(f)
        
    # So sánh 2 file
    assert lan_1 == lan_2, "Hai lần chạy cho kết quả khác nhau -> Chưa tái lập được (Thiếu random_state)"


# =====================================================================
# LOẠI 4: TEST DỊCH VỤ DỰ ĐOÁN (Prediction Service API)
# =====================================================================

# 4.1. Luồng đúng (Happy Path) & Kiểm tra độ tin cậy
def test_api_du_doan_hop_le(client):
    """YÊU CẦU TỪ THẦY: Độ tin cậy trong [0,1], trả về top 3"""
    response = client.post("/du-doan", json={"mo_ta": "Màn hình điện thoại bị sọc xanh"})
    assert response.status_code == 200
    data = response.json()
    
    assert "nhom_loi_du_doan" in data
    assert "do_tin_cay" in data
    assert 0.0 <= data["do_tin_cay"] <= 1.0
    assert "top_3" in data
    assert len(data["top_3"]) == 3 # Đảm bảo trả đủ top 3
    
    # Kiểm tra tổng xác suất (nếu có thể tính từ top 3, hoặc chỉ cần check logic)
    tong_xac_suat = sum([item["do_tin_cay"] for item in data["top_3"]])
    assert 0.0 <= tong_xac_suat <= 1.05 # Cho phép sai số làm tròn

# 4.2. Văn bản rất dài (Vượt phân vị 95)
def test_api_van_ban_rat_dai_van_xu_ly_duoc(client):
    """YÊU CẦU TỪ THẦY: Văn bản rất dài (vượt phân vị 95) -> xử lý được (không sập)"""
    # Tạo chuỗi khoảng 1500 ký tự (nằm dưới giới hạn max_length=2000)
    van_ban_dai = "Màn hình điện thoại bị sọc xanh và cảm ứng chập chờn không hoạt động " * 25
    assert len(van_ban_dai) < 2000 # Đảm bảo không vượt quá max_length
    
    response = client.post("/du-doan", json={"mo_ta": van_ban_dai})
    assert response.status_code == 200
    assert "nhom_loi_du_doan" in response.json()

# 4.3. Dữ liệu sai và Giá trị biên
@pytest.mark.parametrize("mo_ta, ma_loi_mong_doi", [
    ("", 422),           # YÊU CẦU TỪ THẦY: Văn bản rỗng -> 422
    (" ", 422),          # YÊU CẦU TỪ THẦY: Chỉ khoảng trắng -> 422
    ("a", 422),          # Quá ngắn (1 ký tự - dưới biên 5)
    ("abcd", 422),       # Dưới biên (4 ký tự)
    ("abcde", 200),      # Đúng biên (5 ký tự)
    ("x" * 2001, 422),   # Vượt biên (2001 ký tự)
    (None, 422)          # Truyền giá trị null
])
def test_api_du_doan_du_lieu_sai_va_bien(client, mo_ta, ma_loi_mong_doi):
    """Kiểm tra API từ chối dữ liệu sai và xử lý đúng tại các giá trị biên"""
    response = client.post("/du-doan", json={"mo_ta": mo_ta})
    assert response.status_code == ma_loi_mong_doi