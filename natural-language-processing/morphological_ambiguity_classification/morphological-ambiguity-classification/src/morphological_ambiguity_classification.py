import re
import warnings
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
from openpyxl.drawing.image import Image as XLImage
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from transformers import BertTokenizer, TFBertModel


RANDOM_STATE = 42
BERT_MODEL_NAME = "dbmdz/bert-base-turkish-cased"


def get_project_paths() -> dict[str, Path]:
    """Create and return all project paths."""
    project_root = Path(__file__).resolve().parents[1]

    paths = {
        "project_root": project_root,
        "data_dir": project_root / "data",
        "outputs_dir": project_root / "outputs",
        "artifacts_dir": project_root / "artifacts",
        "visualizations_dir": project_root / "outputs" / "visualizations",
        "dataset_xlsx": project_root / "data" / "turkish_labeled_dataset.xlsx",
        "test_words": project_root / "data" / "test_words.txt",
        "predictions_xlsx": project_root / "outputs" / "predictions.xlsx",
        "tfidf_vectorizer": project_root / "artifacts" / "tfidf_vectorizer.pkl",
        "bert_train": project_root / "artifacts" / "bert_embeddings_train.npy",
        "bert_test": project_root / "artifacts" / "bert_embeddings_test.npy",
        "bert_external_test": project_root / "artifacts" / "bert_embeddings_external_test.npy",
        "rf_confusion_matrix": project_root / "outputs" / "visualizations" / "random_forest_confusion_matrix.png",
        "dl_confusion_matrix": project_root / "outputs" / "visualizations" / "deep_learning_confusion_matrix.png",
        "dl_loss_curve": project_root / "outputs" / "visualizations" / "deep_learning_loss_curve.png",
        "dl_accuracy_curve": project_root / "outputs" / "visualizations" / "deep_learning_accuracy_curve.png",
    }

    paths["outputs_dir"].mkdir(parents=True, exist_ok=True)
    paths["artifacts_dir"].mkdir(parents=True, exist_ok=True)
    paths["visualizations_dir"].mkdir(parents=True, exist_ok=True)

    return paths


def load_and_preprocess_data(dataset_path: Path, sheet_name: str = "Organised Data") -> pd.DataFrame:
    """Load the dataset and normalize labels."""
    df_excel = pd.read_excel(
        dataset_path,
        sheet_name=sheet_name,
        usecols=["Kelime", "Etiket"],
        engine="openpyxl"
    )

    words: list[str] = []
    labels: list[str] = []

    for _, row in df_excel.iterrows():
        word = str(row["Kelime"]).strip()
        label_text = str(row["Etiket"]).strip()

        if not word or word.lower() == "nan":
            continue
        if not label_text or label_text.lower() == "nan":
            continue

        # Extract labels inside brackets and split them by comma
        match = re.search(r"\[(.*?)\]", label_text)
        if match:
            label_content = match.group(1)
            label_parts = [item.strip() for item in label_content.split(",") if item.strip()]

            for item in label_parts:
                tag = item.split(":")[1].strip() if ":" in item else item.strip()
                words.append(word)
                labels.append(tag)
        else:
            words.append(word)
            labels.append(label_text)

    df = pd.DataFrame({"word": words, "label": labels})
    df = df.dropna().drop_duplicates().reset_index(drop=True)
    return df


def encode_labels(df: pd.DataFrame, min_samples: int = 5) -> tuple[pd.DataFrame, LabelEncoder]:
    """Remove low-frequency classes and encode labels."""
    class_counts = df["label"].value_counts()
    valid_classes = class_counts[class_counts >= min_samples].index

    df_filtered = df[df["label"].isin(valid_classes)].copy().reset_index(drop=True)

    label_encoder = LabelEncoder()
    df_filtered["label_encoded"] = label_encoder.fit_transform(df_filtered["label"])

    return df_filtered, label_encoder


def load_test_words(test_path: Path) -> list[str]:
    """Load external test words from a text file."""
    with open(test_path, "r", encoding="utf-8") as file:
        text = file.read()

    return [word.strip() for word in text.split() if word.strip()]


def get_bert_model() -> tuple[BertTokenizer, TFBertModel]:
    """Load the BERT tokenizer and model."""
    tokenizer = BertTokenizer.from_pretrained(BERT_MODEL_NAME)
    model = TFBertModel.from_pretrained(BERT_MODEL_NAME)
    return tokenizer, model


def get_bert_embeddings(
    texts: list[str],
    tokenizer: BertTokenizer,
    bert_model: TFBertModel,
    cache_path: Path | None = None,
    batch_size: int = 256
) -> np.ndarray:
    """Generate BERT CLS embeddings and optionally cache them."""
    if cache_path and cache_path.exists():
        cached = np.load(cache_path)
        if len(cached) == len(texts):
            return cached

    embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        inputs = tokenizer(batch, return_tensors="tf", truncation=True, padding=True)
        outputs = bert_model(inputs)
        cls_output = outputs.last_hidden_state[:, 0, :].numpy()
        embeddings.append(cls_output)

    embeddings_array = np.vstack(embeddings)

    if cache_path:
        np.save(cache_path, embeddings_array)

    return embeddings_array


def build_features(
    train_texts: list[str],
    test_texts: list[str],
    paths: dict[str, Path]
) -> tuple[np.ndarray, np.ndarray, TfidfVectorizer]:
    """
    Build TF-IDF + BERT features.

    Important:
    TF-IDF is fitted only on the training set to prevent data leakage.
    """
    tfidf = TfidfVectorizer(
        lowercase=True,
        analyzer="char_wb",
        ngram_range=(2, 4),
        min_df=2
    )

    x_train_tfidf = tfidf.fit_transform(train_texts).toarray()
    x_test_tfidf = tfidf.transform(test_texts).toarray()

    joblib.dump(tfidf, paths["tfidf_vectorizer"])

    tokenizer, bert_model = get_bert_model()

    train_bert = get_bert_embeddings(
        texts=train_texts,
        tokenizer=tokenizer,
        bert_model=bert_model,
        cache_path=paths["bert_train"]
    )

    test_bert = get_bert_embeddings(
        texts=test_texts,
        tokenizer=tokenizer,
        bert_model=bert_model,
        cache_path=paths["bert_test"]
    )

    x_train = np.hstack((x_train_tfidf, train_bert))
    x_test = np.hstack((x_test_tfidf, test_bert))

    return x_train, x_test, tfidf


def train_random_forest(x_train: np.ndarray, y_train: np.ndarray, cv_folds: int = 3) -> RandomForestClassifier:
    """Train a Random Forest model with grid search."""
    model = RandomForestClassifier(
        random_state=RANDOM_STATE,
        class_weight="balanced",
        n_jobs=-1
    )

    param_grid = {
        "n_estimators": [200, 300],
        "max_depth": [20, 40, None],
        "min_samples_split": [2, 5],
        "min_samples_leaf": [1, 2]
    }

    grid_search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        cv=cv_folds,
        scoring="f1_weighted",
        n_jobs=-1,
        verbose=1
    )
    grid_search.fit(x_train, y_train)
    return grid_search.best_estimator_


def train_deep_learning(
    x_train: np.ndarray,
    y_train: np.ndarray,
    num_classes: int,
    epochs: int = 30,
    batch_size: int = 128
) -> tuple[Sequential, tf.keras.callbacks.History]:
    """Train the deep learning classifier."""
    input_dim = x_train.shape[1]

    class_weights = compute_class_weight(
        class_weight="balanced",
        classes=np.unique(y_train),
        y=y_train
    )
    class_weight_dict = {int(cls): float(weight) for cls, weight in zip(np.unique(y_train), class_weights)}

    model = Sequential([
        Input(shape=(input_dim,)),
        Dense(512, activation="relu"),
        Dropout(0.4),
        Dense(256, activation="relu"),
        Dropout(0.3),
        Dense(128, activation="relu"),
        Dropout(0.2),
        Dense(num_classes, activation="softmax")
    ])

    model.compile(
        optimizer=Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    callbacks = [
        EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2, min_lr=1e-5)
    ]

    history = model.fit(
        x_train,
        y_train,
        validation_split=0.2,
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        class_weight=class_weight_dict,
        verbose=1
    )

    return model, history


def build_classification_report(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    class_names: list[str]
) -> pd.DataFrame:
    """Create a classification report as a DataFrame."""
    report = classification_report(
        y_true,
        y_pred,
        labels=np.arange(len(class_names)),
        target_names=class_names,
        output_dict=True,
        zero_division=0
    )
    return pd.DataFrame(report).transpose()


def save_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    class_names: list[str],
    output_path: Path,
    title: str
) -> None:
    """Save the confusion matrix as an image."""
    cm = confusion_matrix(y_true, y_pred, labels=np.arange(len(class_names)))
    cm_df = pd.DataFrame(cm, index=class_names, columns=class_names)

    plt.figure(figsize=(14, 12))
    sns.heatmap(cm_df, annot=True, fmt="d", cmap="Blues")
    plt.title(title)
    plt.ylabel("True Label")
    plt.xlabel("Predicted Label")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_training_history(history: tf.keras.callbacks.History, paths: dict[str, Path]) -> None:
    """Plot and save loss and accuracy curves."""
    plt.figure(figsize=(10, 5))
    plt.plot(history.history["loss"], label="Training Loss")
    plt.plot(history.history["val_loss"], label="Validation Loss")
    plt.title("Deep Learning Loss Curve")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.tight_layout()
    plt.savefig(paths["dl_loss_curve"], dpi=300, bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(history.history["accuracy"], label="Training Accuracy")
    plt.plot(history.history["val_accuracy"], label="Validation Accuracy")
    plt.title("Deep Learning Accuracy Curve")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.tight_layout()
    plt.savefig(paths["dl_accuracy_curve"], dpi=300, bbox_inches="tight")
    plt.close()


def predict_test_words(
    test_words: list[str],
    tfidf: TfidfVectorizer,
    rf_model: RandomForestClassifier,
    deep_model: Sequential,
    paths: dict[str, Path]
) -> tuple[np.ndarray, np.ndarray]:
    """Generate predictions for external test words."""
    test_tfidf = tfidf.transform(test_words).toarray()

    tokenizer, bert_model = get_bert_model()
    test_bert = get_bert_embeddings(
        texts=test_words,
        tokenizer=tokenizer,
        bert_model=bert_model,
        cache_path=paths["bert_external_test"]
    )

    x_test_words = np.hstack((test_tfidf, test_bert))

    rf_predictions = rf_model.predict(x_test_words)
    dl_predictions = np.argmax(deep_model.predict(x_test_words, verbose=0), axis=1)

    return rf_predictions, dl_predictions


def save_results_to_excel(
    output_path: Path,
    test_words: list[str],
    rf_external_predictions: np.ndarray,
    dl_external_predictions: np.ndarray,
    label_encoder: LabelEncoder,
    rf_report_df: pd.DataFrame,
    dl_report_df: pd.DataFrame,
    rf_accuracy: float,
    dl_accuracy: float,
    paths: dict[str, Path]
) -> None:
    """Save predictions, reports, accuracies, and confusion matrices into a single Excel file."""
    predictions_df = pd.DataFrame({
        "Input": test_words,
        "RandomForest_Prediction": label_encoder.inverse_transform(rf_external_predictions),
        "DeepLearning_Prediction": label_encoder.inverse_transform(dl_external_predictions)
    })

    accuracy_df = pd.DataFrame({
        "Model": ["Random Forest", "Deep Learning"],
        "Accuracy": [rf_accuracy, dl_accuracy]
    })

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        predictions_df.to_excel(writer, sheet_name="Predictions", index=False)
        accuracy_df.to_excel(writer, sheet_name="Accuracy", index=False)
        rf_report_df.to_excel(writer, sheet_name="RandomForest_Report")
        dl_report_df.to_excel(writer, sheet_name="DeepLearning_Report")

        rf_sheet = writer.sheets["RandomForest_Report"]
        dl_sheet = writer.sheets["DeepLearning_Report"]

        rf_image = XLImage(str(paths["rf_confusion_matrix"]))
        rf_image.anchor = "L2"
        rf_sheet.add_image(rf_image)

        dl_image = XLImage(str(paths["dl_confusion_matrix"]))
        dl_image.anchor = "L2"
        dl_sheet.add_image(dl_image)


def main() -> None:
    """Run the full morphological ambiguity classification pipeline."""
    warnings.filterwarnings("ignore")
    tf.random.set_seed(RANDOM_STATE)
    np.random.seed(RANDOM_STATE)

    paths = get_project_paths()

    df = load_and_preprocess_data(paths["dataset_xlsx"], sheet_name="Organised Data")
    df, label_encoder = encode_labels(df, min_samples=5)

    x_text = df["word"].tolist()
    y = df["label_encoded"].values

    x_train_text, x_test_text, y_train, y_test = train_test_split(
        x_text,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y
    )

    x_train, x_test, tfidf = build_features(x_train_text, x_test_text, paths)

    print(f"Training set shape: {x_train.shape}")
    print(f"Test set shape: {x_test.shape}")

    print("Training Random Forest...")
    rf_model = train_random_forest(x_train, y_train, cv_folds=3)
    y_pred_rf = rf_model.predict(x_test)

    print("Training Deep Learning model...")
    deep_model, history = train_deep_learning(
        x_train=x_train,
        y_train=y_train,
        num_classes=len(label_encoder.classes_),
        epochs=30,
        batch_size=128
    )
    y_pred_dl = np.argmax(deep_model.predict(x_test, verbose=0), axis=1)

    class_names = list(label_encoder.classes_)

    rf_report_df = build_classification_report(y_test, y_pred_rf, class_names)
    dl_report_df = build_classification_report(y_test, y_pred_dl, class_names)

    rf_accuracy = accuracy_score(y_test, y_pred_rf)
    dl_accuracy = accuracy_score(y_test, y_pred_dl)

    print(f"Random Forest Accuracy: {rf_accuracy:.4f}")
    print(f"Deep Learning Accuracy: {dl_accuracy:.4f}")

    save_confusion_matrix(
        y_true=y_test,
        y_pred=y_pred_rf,
        class_names=class_names,
        output_path=paths["rf_confusion_matrix"],
        title="Random Forest Confusion Matrix"
    )

    save_confusion_matrix(
        y_true=y_test,
        y_pred=y_pred_dl,
        class_names=class_names,
        output_path=paths["dl_confusion_matrix"],
        title="Deep Learning Confusion Matrix"
    )

    plot_training_history(history, paths)

    external_test_words = load_test_words(paths["test_words"])
    rf_external_predictions, dl_external_predictions = predict_test_words(
        test_words=external_test_words,
        tfidf=tfidf,
        rf_model=rf_model,
        deep_model=deep_model,
        paths=paths
    )

    save_results_to_excel(
        output_path=paths["predictions_xlsx"],
        test_words=external_test_words,
        rf_external_predictions=rf_external_predictions,
        dl_external_predictions=dl_external_predictions,
        label_encoder=label_encoder,
        rf_report_df=rf_report_df,
        dl_report_df=dl_report_df,
        rf_accuracy=rf_accuracy,
        dl_accuracy=dl_accuracy,
        paths=paths
    )

    print(f"Results saved to: {paths['predictions_xlsx']}")
    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()