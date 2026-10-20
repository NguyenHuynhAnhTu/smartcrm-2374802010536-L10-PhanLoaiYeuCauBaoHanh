import argparse
import hashlib
import json
from importlib.metadata import version
from pathlib import Path

import joblib
import pandas as pd
import yaml
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import ComplementNB

from src.features.text import clean_text


ROOT = Path(__file__).resolve().parents[2]


def resolve_path(path_value):
    """Chuyển đường dẫn tương đối thành đường dẫn từ thư mục gốc dự án."""
    path = Path(path_value)
    return path if path.is_absolute() else ROOT / path


def load_config(config_path):
    """Đọc cấu hình YAML."""
    path = resolve_path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy file cấu hình: {path}")

    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError("Nội dung file cấu hình không hợp lệ.")

    return config


def load_dataset(config):
    """Đọc và kiểm tra dữ liệu trước khi chia tập."""
    path = resolve_path(config["data_path"])

    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy dataset: {path}")

    df = pd.read_csv(path)
    text_col = config["text_column"]
    target_col = config["target_column"]

    for column in (text_col, target_col):
        if column not in df.columns:
            raise ValueError(f"Dataset thiếu cột bắt buộc: {column}")

    if df.empty:
        raise ValueError("Dataset không có dữ liệu.")

    if df[target_col].isna().any():
        raise ValueError("Cột nhãn có giá trị trống.")

    df = df[[text_col, target_col]].copy()
    df[text_col] = df[text_col].map(
        lambda value: clean_text(value)
    )
    df[target_col] = df[target_col].astype(str).str.strip()

    if (df[target_col] == "").any():
        raise ValueError("Cột nhãn có giá trị rỗng.")

    expected = set(config["expected_labels"])
    actual = set(df[target_col].unique())

    missing_labels = sorted(expected - actual)
    unexpected_labels = sorted(actual - expected)

    if missing_labels or unexpected_labels:
        raise ValueError(
            f"Nhãn thiếu trong dữ liệu: {missing_labels}; "
            f"nhãn ngoài danh sách: {unexpected_labels}"
        )

    return df, path


def split_dataset(df, config):
    """Chia train, validation và test có phân tầng theo nhãn."""
    target_col = config["target_column"]
    seed = int(config["seed"])
    split = config["split"]

    train_ratio = float(split["train"])
    val_ratio = float(split["validation"])
    test_ratio = float(split["test"])

    if abs(train_ratio + val_ratio + test_ratio - 1.0) > 1e-9:
        raise ValueError("Tỷ lệ chia tập phải có tổng bằng 1.")

    if min(train_ratio, val_ratio, test_ratio) <= 0:
        raise ValueError("Mỗi tập dữ liệu phải có tỷ lệ lớn hơn 0.")

    train_df, remaining_df = train_test_split(
        df,
        test_size=val_ratio + test_ratio,
        random_state=seed,
        stratify=df[target_col],
    )

    test_ratio_remaining = test_ratio / (val_ratio + test_ratio)

    val_df, test_df = train_test_split(
        remaining_df,
        test_size=test_ratio_remaining,
        random_state=seed,
        stratify=remaining_df[target_col],
    )

    return train_df, val_df, test_df


def calculate_basic_metrics(y_true, y_pred):
    """Tính Accuracy và Macro F1."""
    return {
        "accuracy": round(
            float(accuracy_score(y_true, y_pred)), 4
        ),
        "f1_macro": round(
            float(
                f1_score(
                    y_true,
                    y_pred,
                    average="macro",
                    zero_division=0,
                )
            ),
            4,
        ),
    }


def analyze_confusion_matrix(matrix, labels, recalls):
    """Tạo ba nhận xét ban đầu từ ma trận nhầm lẫn."""
    pairs = []

    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            errors = int(matrix[i, j] + matrix[j, i])
            pairs.append({
                "label_a": labels[i],
                "label_b": labels[j],
                "errors_in_both_directions": errors,
            })

    most_confused_pair = max(
        pairs, key=lambda item: item["errors_in_both_directions"]
    )

    lowest_recall_index = min(
        range(len(labels)), key=lambda i: recalls[i]
    )

    false_positive_counts = {
        labels[j]: int(matrix[:, j].sum() - matrix[j, j])
        for j in range(len(labels))
    }
    possible_garbage_label = max(
        false_positive_counts, key=false_positive_counts.get
    )

    if false_positive_counts[possible_garbage_label] == 0:
        garbage_note = (
            "Không có dự đoán sai từ nhãn khác đổ vào một nhãn."
        )
        possible_garbage_label = None
    else:
        garbage_note = (
            "Đây chỉ là dấu hiệu cần kiểm tra thêm; "
            "không tự động kết luận nhãn này là nhãn thùng rác."
        )

    return {
        "most_confused_pair": most_confused_pair,
        "lowest_recall_label": {
            "label": labels[lowest_recall_index],
            "recall": round(
                float(recalls[lowest_recall_index]), 4
            ),
        },
        "possible_garbage_label": possible_garbage_label,
        "false_positive_predictions_by_label": false_positive_counts,
        "garbage_label_note": garbage_note,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Huấn luyện và đánh giá mô hình phân loại sự cố."
    )
    parser.add_argument(
        "--config",
        default="configs/train.yaml",
        help="Đường dẫn đến file cấu hình YAML.",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    df, data_path = load_dataset(config)

    text_col = config["text_column"]
    target_col = config["target_column"]
    labels = list(config["expected_labels"])
    seed = int(config["seed"])

    train_df, val_df, test_df = split_dataset(df, config)

    print("=== KÍCH THƯỚC CÁC TẬP ===")
    print(f"Train:      {len(train_df)}")
    print(f"Validation: {len(val_df)}")
    print(f"Test:       {len(test_df)}")

    # Chỉ fit TF-IDF trên train để tránh rò rỉ dữ liệu.
    vectorizer_config = config["vectorizer"]
    vectorizer = TfidfVectorizer(
        ngram_range=(
            int(vectorizer_config["ngram_min"]),
            int(vectorizer_config["ngram_max"]),
        ),
        min_df=int(vectorizer_config["min_df"]),
        max_features=int(vectorizer_config["max_features"]),
    )

    X_train = vectorizer.fit_transform(train_df[text_col])
    X_val = vectorizer.transform(val_df[text_col])
    X_test = vectorizer.transform(test_df[text_col])

    y_train = train_df[target_col]
    y_val = val_df[target_col]
    y_test = test_df[target_col]

    # Baseline: luôn dự đoán nhãn phổ biến nhất của train.
    dummy = DummyClassifier(strategy="most_frequent")
    dummy.fit(X_train, y_train)

    dummy_val_metrics = calculate_basic_metrics(
        y_val, dummy.predict(X_val)
    )

    # Hai mô hình thực để so sánh trên validation.
    candidates = {
        "logistic_regression": LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=seed,
        ),
        "complement_nb": ComplementNB(),
    }

    validation_results = {
        "dummy_most_frequent": dummy_val_metrics
    }

    for name, model in candidates.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_val)
        validation_results[name] = calculate_basic_metrics(
            y_val, predictions
        )

    print("\n=== SO SÁNH TRÊN VALIDATION ===")
    for name, result in validation_results.items():
        print(
            f"{name:24s} "
            f"Macro F1 = {result['f1_macro']:.4f} | "
            f"Accuracy = {result['accuracy']:.4f}"
        )

    # Chọn trong hai mô hình thực, không dùng test để lựa chọn.
    selected_name = max(
        candidates,
        key=lambda name: validation_results[name]["f1_macro"],
    )
    selected_model = candidates[selected_name]

    print(f"\nMô hình được chọn: {selected_name}")

    # Đánh giá test ở giai đoạn cuối sau khi đã chọn mô hình.
    # Không dùng kết quả test để quay lại chọn mô hình.
    test_predictions = selected_model.predict(X_test)

    test_basic_metrics = calculate_basic_metrics(
        y_test, test_predictions
    )

    matrix = confusion_matrix(
        y_test, test_predictions, labels=labels
    )

    precision, recall, f1, support = (
        precision_recall_fscore_support(
            y_test,
            test_predictions,
            labels=labels,
            zero_division=0,
        )
    )

    per_label_metrics = {}
    for i, label in enumerate(labels):
        per_label_metrics[label] = {
            "precision": round(float(precision[i]), 4),
            "recall": round(float(recall[i]), 4),
            "f1": round(float(f1[i]), 4),
            "support": int(support[i]),
        }

    conclusions = analyze_confusion_matrix(
        matrix, labels, recall
    )

    data_hash = hashlib.sha256(data_path.read_bytes()).hexdigest()
    label_counts = df[target_col].value_counts()

    metrics = {
        "project": config.get("project_name", "smartcrm-l10"),
        "seed": seed,
        "dataset": {
            "file": str(data_path.relative_to(ROOT)),
            "sha256": data_hash,
            "rows": int(len(df)),
            "text_column": text_col,
            "target_column": target_col,
            "label_distribution": {
                label: int(label_counts.get(label, 0))
                for label in labels
            },
            "empty_description_count": int(
                (df[text_col] == "").sum()
            ),
            "ignored_labels": [],
        },
        "split_sizes": {
            "train": int(len(train_df)),
            "validation": int(len(val_df)),
            "test": int(len(test_df)),
        },
        "vectorizer": {
            "type": "TfidfVectorizer",
            "ngram_range": [
                int(vectorizer_config["ngram_min"]),
                int(vectorizer_config["ngram_max"]),
            ],
            "min_df": int(vectorizer_config["min_df"]),
            "max_features": int(
                vectorizer_config["max_features"]
            ),
            "fit_on": "train_only",
        },
        "library_versions": {
            "pandas": version("pandas"),
            "numpy": version("numpy"),
            "scikit_learn": version("scikit-learn"),
            "joblib": version("joblib"),
            "PyYAML": version("PyYAML"),
        },
        "validation_comparison": validation_results,
        "selected_model": {
            "name": selected_name,
            "selection_metric": "validation_macro_f1",
            "validation_metrics": validation_results[selected_name],
        },
        "test": {
            **test_basic_metrics,
            "labels_order": labels,
            "per_label": per_label_metrics,
            "confusion_matrix": matrix.tolist(),
            "conclusions": conclusions,
        },
    }

    artifact_path = resolve_path(config["output_artifact"])
    artifact_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(
        {
            "vectorizer": vectorizer,
            "model": selected_model,
            "labels": labels,
            "selected_model": selected_name,
            "seed": seed,
            "data_sha256": data_hash,
        },
        artifact_path,
    )

    metrics_path = resolve_path(config["output_metrics"])
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    with metrics_path.open("w", encoding="utf-8") as file:
        json.dump(metrics, file, ensure_ascii=False, indent=2)

    print("\n=== KẾT QUẢ TEST CUỐI CÙNG ===")
    print(f"Accuracy: {test_basic_metrics['accuracy']:.4f}")
    print(f"Macro F1: {test_basic_metrics['f1_macro']:.4f}")
    print(f"Báo cáo: {metrics_path.relative_to(ROOT)}")
    print(f"Mô hình: {artifact_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()