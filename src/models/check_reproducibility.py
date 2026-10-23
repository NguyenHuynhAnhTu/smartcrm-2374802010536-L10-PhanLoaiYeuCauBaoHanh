
import hashlib
import json
from pathlib import Path

from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import ComplementNB

from src.models.train import (
    load_config,
    load_dataset,
    split_dataset,
    calculate_basic_metrics,
)


ROOT = Path(__file__).resolve().parents[2]


def run_validation(df, config):
    """Huấn luyện và đánh giá trên validation, không đánh giá test."""
    text_col = config["text_column"]
    target_col = config["target_column"]
    seed = int(config["seed"])

    train_df, val_df, _ = split_dataset(df, config)

    vectorizer_config = config["vectorizer"]

    vectorizer = TfidfVectorizer(
        ngram_range=(
            int(vectorizer_config["ngram_min"]),
            int(vectorizer_config["ngram_max"]),
        ),
        min_df=int(vectorizer_config["min_df"]),
        max_features=int(vectorizer_config["max_features"]),
    )

    # Chỉ học từ vựng TF-IDF trên train.
    X_train = vectorizer.fit_transform(train_df[text_col])
    X_val = vectorizer.transform(val_df[text_col])

    y_train = train_df[target_col]
    y_val = val_df[target_col]

    models = {
        "dummy_most_frequent": DummyClassifier(
            strategy="most_frequent"
        ),
        "logistic_regression": LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=seed,
        ),
        "complement_nb": ComplementNB(),
    }

    results = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_val)

        results[name] = calculate_basic_metrics(
            y_val, predictions
        )

    return results


def main():
    config = load_config("configs/train.yaml")
    df, data_path = load_dataset(config)

    print("Lần chạy 1: kiểm tra train/validation...")
    result_1 = run_validation(df, config)

    print("Lần chạy 2: kiểm tra train/validation...")
    result_2 = run_validation(df, config)

    identical = result_1 == result_2

    report = {
        "seed": int(config["seed"]),
        "dataset_sha256": hashlib.sha256(
            data_path.read_bytes()
        ).hexdigest(),
        "scope": "Train/validation only; test not evaluated",
        "run_1": result_1,
        "run_2": result_2,
        "identical": identical,
    }

    output_path = ROOT / "reports" / "reproducibility_check.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)

    print("\n=== KẾT QUẢ KIỂM TRA TÍNH TÁI LẬP ===")
    print(f"Seed: {config['seed']}")
    print(f"Hai lần chạy giống nhau: {identical}")
    print(f"Báo cáo: {output_path.relative_to(ROOT)}")

    if not identical:
        raise SystemExit(
            "Kết quả validation khác nhau. "
            "Hãy kiểm tra seed, dữ liệu và phiên bản thư viện."
        )


if __name__ == "__main__":
    main()
