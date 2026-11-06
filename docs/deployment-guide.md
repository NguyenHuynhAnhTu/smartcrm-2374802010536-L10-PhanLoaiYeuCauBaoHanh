# Deployment Guide

## 1. System Requirements
Requires Docker Desktop installed and running. Git is required to clone the repository.

## 2. Installation Instructions
Clone the repository: `git clone https://github.com/NguyenHuynhAnhTu/smartcrm-2374802010536-L10-PhanLoaiYeuCauBaoHanh.git`
Navigate to the directory: `cd smartcrm-2374802010536-L10-PhanLoaiYeuCauBaoHanh`

## 3. Execution Instructions
Run the command: `docker compose up -d --build`. This builds the image, installs dependencies, and starts the API.

## 4. System Verification
Run `docker compose ps` and ensure the status is "Up (healthy)". Access the UI at `http://127.0.0.1:8000/`.

## 5. Teardown
Run `docker compose down` to stop the system.

## 6. Security Checklist
1. Sensitive configs (Base URL, Port) use `.env`.
2. Real `.env` is ignored by Git.
3. Input Validation via Pydantic (`min_length=5`).
4. PII (Phone numbers) masked via `clean_text`.
5. Docker runs as non-root `appuser`.
6. Error messages don't leak stack traces.
7. Model files (`*.joblib`) are ignored by Git.