import re


# Nhận diện email, số điện thoại và mã serial có chữ và số.
EMAIL_PATTERN = re.compile(
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
    re.IGNORECASE,
)

PHONE_PATTERN = re.compile(
    r"(?<!\w)(?:\+?84|0)(?:[\s.-]?\d){8,10}(?!\w)"
)

SERIAL_PATTERN = re.compile(
    r"\b(?=[A-Z0-9-]{8,24}\b)"
    r"(?=[A-Z0-9-]*[A-Z])"
    r"(?=[A-Z0-9-]*\d)"
    r"[A-Z0-9-]+\b",
    re.IGNORECASE,
)


def clean_text(text):
    """
    Hợp đồng:
    - Đầu vào: mô tả lỗi dạng chuỗi hoặc None.
    - Đầu ra: chuỗi đã làm sạch.
    - Giữ nguyên dấu tiếng Việt, chuyển chữ thường.
    - Thay email, số điện thoại và mã serial bằng token.
    - Đầu vào None hoặc không có nội dung -> chuỗi rỗng.
    """
    if text is None:
        return ""

    text = str(text).strip().lower()

    if not text:
        return ""

    text = EMAIL_PATTERN.sub("<email>", text)
    text = PHONE_PATTERN.sub("<phone>", text)
    text = SERIAL_PATTERN.sub("<serial>", text)

    # Chuẩn hóa khoảng trắng liên tiếp.
    text = re.sub(r"\s+", " ", text).strip()

    return text