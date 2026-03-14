from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Tuple
import logging
import random

import stanza
from stop_words import get_stop_words


@dataclass
class Document:
    author: str
    filename: str
    text: str


def configure_logging(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / f"preprocessing_results_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_path, encoding="utf-8"),
        ],
    )


def read_text_file(file_path: Path) -> str:
    encodings = ["utf-8", "utf-8-sig", "utf-16", "cp1254", "iso-8859-9", "latin-1"]

    for encoding in encodings:
        try:
            return file_path.read_text(encoding=encoding).strip()
        except UnicodeError:
            continue
        except OSError:
            continue

    raise ValueError(f"Could not decode file with supported encodings: {file_path}")


def load_documents(data_dir: Path) -> List[Document]:
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    documents: List[Document] = []
    author_dirs = sorted(path for path in data_dir.iterdir() if path.is_dir())

    for author_dir in author_dirs:
        text_files = sorted(author_dir.glob("*.txt"))

        for text_file in text_files:
            text = read_text_file(text_file)
            if not text:
                continue

            documents.append(
                Document(
                    author=author_dir.name,
                    filename=text_file.name,
                    text=text,
                )
            )

    return documents


def preprocess_text(text: str) -> str:
    text = text.lower()
    return "".join(char if char.isalpha() or char.isspace() else " " for char in text)


def remove_stopwords(text: str, stopwords: set[str]) -> str:
    words = text.split()
    filtered_words = [word for word in words if word not in stopwords]
    return " ".join(filtered_words)


def tokenize_and_lemmatize(text: str, nlp: stanza.Pipeline) -> Tuple[List[str], List[str]]:
    doc = nlp(text)
    tokens: List[str] = []
    lemmas: List[str] = []

    for sentence in doc.sentences:
        for word in sentence.words:
            tokens.append(word.text)
            lemmas.append(word.lemma)

    return tokens, lemmas


def generate_bigrams(tokens: List[str]) -> List[Tuple[str, str]]:
    return list(zip(tokens, tokens[1:]))


def compare_stanza_success(documents: List[Document], nlp: stanza.Pipeline) -> None:
    turkish_stopwords = set(get_stop_words("turkish"))

    for i, document in enumerate(documents, start=1):
        logging.info(f"\n--- Document {i} ---")
        logging.info(f"Author: {document.author}")
        logging.info(f"File: {document.filename}")
        logging.info(f"Original text preview: {document.text[:200]}...")

        preprocessed_text = preprocess_text(document.text)
        cleaned_text = remove_stopwords(preprocessed_text, turkish_stopwords)
        tokens, lemmas = tokenize_and_lemmatize(cleaned_text, nlp)
        bigrams = generate_bigrams(tokens)

        logging.info(f"Preprocessed text preview: {preprocessed_text[:200]}...")
        logging.info(f"Stopwords removed preview: {cleaned_text[:200]}...")
        logging.info(f"Token count: {len(tokens)}")
        logging.info(f"Lemma count: {len(lemmas)}")
        logging.info(f"Bigram count: {len(bigrams)}")
        logging.info(f"First 30 tokens: {tokens[:30]}")
        logging.info(f"First 30 lemmas: {lemmas[:30]}")
        logging.info(f"First 20 bigrams: {bigrams[:20]}")


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / "data" / "raw" / "column_articles"
    output_dir = project_root / "outputs"

    configure_logging(output_dir)

    logging.info("Checking Turkish Stanza resources...")
    stanza.download("tr")

    logging.info("Initializing Stanza pipeline...")
    nlp = stanza.Pipeline("tr", processors="tokenize,mwt,pos,lemma", verbose=False)

    logging.info("Loading documents from data directory...")
    documents = load_documents(data_dir)
    logging.info(f"Total documents loaded: {len(documents)}")

    sampled_documents = random.sample(documents, min(10, len(documents)))
    compare_stanza_success(sampled_documents, nlp)


if __name__ == "__main__":
    main()