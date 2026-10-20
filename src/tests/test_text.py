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
    assert clean_text("") == ""
    assert clean_text("   ") == ""
    assert clean_text(None) == ""