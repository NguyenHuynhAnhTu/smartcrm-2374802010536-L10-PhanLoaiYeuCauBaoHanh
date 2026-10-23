from src.features.text import clean_text


def test_lowercase_and_keep_vietnamese_diacritics():
    result = clean_text("  MÀN HÌNH   NHẤP NHÁY  ")

    assert result == "màn hình nhấp nháy"


def test_mask_personal_information():
    result = clean_text(
        "Liên hệ 0912345678 hoặc abc@gmail.com, mã SN12345678"
    )

    assert "<phone>" in result
    assert "<email>" in result
    assert "<serial>" in result


def test_empty_input():
    """Chuỗi rỗng và chuỗi chỉ có khoảng trắng được xử lý."""
    assert clean_text("") == ""
    assert clean_text("   ") == ""


def test_none_input_is_handled():
    """Đầu vào None được xử lý an toàn."""
    assert clean_text(None) == ""



def test_chuan_hoa_khoang_trang():
    """Khoảng trắng và xuống dòng được chuẩn hóa."""
    mo_ta = "  Máy   bị\n\nNÓNG  "

    ket_qua = clean_text(mo_ta)

    assert ket_qua == "máy bị nóng"


def test_mo_ta_dai_khong_bi_cat():
    """Mô tả dài vẫn được giữ đầy đủ sau khi chuẩn hóa."""
    mo_ta = "Máy bị lỗi " * 100

    ket_qua = clean_text(mo_ta)

    mong_doi = " ".join(["máy", "bị", "lỗi"] * 100)
    assert ket_qua == mong_doi
