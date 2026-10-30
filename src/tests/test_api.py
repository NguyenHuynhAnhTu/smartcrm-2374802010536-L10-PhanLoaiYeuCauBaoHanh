import pytest
from fastapi.testclient import TestClient
from src.serve.app import app

# Sử dụng fixture để đảm bảo app được khởi động (chạy lifespan nạp model)
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_predict_happy_path(client):
    # Gửi 1 câu hợp lệ (>5 ký tự)
    response = client.post("/du-doan", json={"mo_ta": "Màn hình điện thoại bị sọc xanh"})
    assert response.status_code == 200
    data = response.json()
    assert "nhom_loi_du_doan" in data
    assert "top_3" in data
    assert "do_tin_cay" in data

def test_predict_bad_data(client):
    # Gửi câu quá ngắn (<5 ký tự) -> Pydantic phải chặn và trả về 422
    response = client.post("/du-doan", json={"mo_ta": "Hỏng"})
    assert response.status_code == 422 

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"