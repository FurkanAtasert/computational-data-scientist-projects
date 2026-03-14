from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import nltk
import pandas as pd
import string
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

N_COMPONENTS = 5
TOP_TERMS_TEXT = 15
TOP_TERMS_PLOT = 10


def ensure_nltk_resources() -> None:
    try:
        stopwords.words("turkish")
    except LookupError:
        nltk.download("stopwords")


def load_documents(file_path: Path) -> List[str]:
    if not file_path.exists():
        raise FileNotFoundError(f"Document file not found: {file_path}")

    documents = []
    with file_path.open("r", encoding="utf-8") as file:
        for line in file:
            text = line.strip()
            if text:
                documents.append(text)

    return documents


def build_stopwords() -> set[str]:
    base_stopwords = set(stopwords.words("turkish"))
    additional_stopwords = {"her", "daha", "gibi", "var", "ve", "için"}
    return base_stopwords.union(additional_stopwords)


def preprocess_document(document: str, stopword_set: set[str]) -> str:
    document = document.lower()
    translator = str.maketrans("", "", string.punctuation)
    document = document.translate(translator)

    tokenizer = RegexpTokenizer(r"\w+")
    words = tokenizer.tokenize(document)
    words = [word for word in words if word not in stopword_set]

    return " ".join(words)


def save_topic_terms(lsa: TruncatedSVD, terms: List[str], output_dir: Path) -> None:
    for topic_index, component in enumerate(lsa.components_, start=1):
        sorted_terms = sorted(zip(terms, component), key=lambda x: x[1], reverse=True)

        topic_file = output_dir / f"topic_{topic_index}_terms.txt"
        with topic_file.open("w", encoding="utf-8") as file:
            for term, weight in sorted_terms[:TOP_TERMS_TEXT]:
                file.write(f"{term}: {weight:.4f}\n")

        top_terms = sorted_terms[:TOP_TERMS_PLOT]
        term_names = [term for term, _ in top_terms]
        term_weights = [weight for _, weight in top_terms]

        plt.figure(figsize=(10, 6))
        plt.barh(term_names, term_weights)
        plt.gca().invert_yaxis()
        plt.xlabel("Weight")
        plt.title(f"Topic {topic_index} Terms")
        plt.tight_layout()
        plt.savefig(output_dir / f"topic_{topic_index}_terms.png")
        plt.close()


def save_document_topic_distribution(
    lsa: TruncatedSVD,
    dtm,
    documents: List[str],
    output_dir: Path,
) -> None:
    document_topic_matrix = lsa.transform(dtm)
    df_document_topic = pd.DataFrame(
        document_topic_matrix,
        columns=[f"topic_{i + 1}" for i in range(document_topic_matrix.shape[1])],
    )
    df_document_topic["document"] = documents
    df_document_topic.to_csv(output_dir / "document_topic_distribution.csv", index=False, encoding="utf-8")


def main() -> None:
    ensure_nltk_resources()

    project_root = Path(__file__).resolve().parent.parent
    data_file = project_root / "data" / "sample_documents.txt"
    output_dir = project_root / "outputs" / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_dir.mkdir(parents=True, exist_ok=True)

    documents = load_documents(data_file)
    stopword_set = build_stopwords()
    processed_documents = [preprocess_document(document, stopword_set) for document in documents]

    print("Processed Documents:")
    for document in processed_documents:
        print(document)

    vectorizer = TfidfVectorizer()
    dtm = vectorizer.fit_transform(processed_documents)
    terms = vectorizer.get_feature_names_out().tolist()

    print("\nTerms:")
    print(terms)

    lsa = TruncatedSVD(n_components=N_COMPONENTS, n_iter=100, random_state=42)
    lsa.fit(dtm)

    save_topic_terms(lsa, terms, output_dir)
    save_document_topic_distribution(lsa, dtm, documents, output_dir)

    print(f"\nResults were saved to: {output_dir}")


if __name__ == "__main__":
    main()