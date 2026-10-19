from pathlib import Path

import pandas as pd


def load_dataset():
    """Đọc dataset mô tả yêu cầu bảo hành."""
    project_root = Path(__file__).resolve().parents[2]
    data_path = project_root / "data" / "issue_descriptions.csv"

    if not data_path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy dataset: {data_path}"
        )

    df = pd.read_csv(data_path)

    return df


def main():
    """Nạp dữ liệu và in báo cáo kiểm tra cơ bản."""
    df = load_dataset()

    print("=== BÁO CÁO NẠP DATASET ===")
    print(f"Đường dẫn: data/issue_descriptions.csv")
    print(f"Số dòng: {df.shape[0]}")
    print(f"Số cột: {df.shape[1]}")

    print("\n=== DANH SÁCH CỘT ===")
    print(df.columns.tolist())

    print("\n=== SỐ Ô TRỐNG TỪNG CỘT ===")
    print(df.isna().sum().to_string())

    if "issue_category" in df.columns:
        print("\n=== PHÂN BỐ NHÃN ===")
        print(df["issue_category"].value_counts().to_string())

        print("\n=== TỶ LỆ NHÃN (%) ===")
        print(
            (
                df["issue_category"]
                .value_counts(normalize=True)
                .mul(100)
                .round(2)
            ).to_string()
        )

    print("\n=== 5 DÒNG DỮ LIỆU ĐẦU ===")
    print(df.head().to_string(index=False))


if __name__ == "__main__":
    main()