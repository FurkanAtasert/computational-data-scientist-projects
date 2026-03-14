# Turkish Text Preprocessing with Stanza

This project demonstrates a Turkish text preprocessing pipeline using Stanza.  
It processes a collection of Turkish column articles, applies normalization, stopword removal, tokenization, lemmatization, and bigram extraction, and logs the results for a random sample of documents.

## Project Overview

The dataset consists of Turkish column articles grouped by author.  
The pipeline is designed to:

- load text files from the dataset directory
- normalize raw text
- remove Turkish stopwords
- tokenize text using Stanza
- extract lemmas
- generate bigrams
- save preprocessing results into log files

This project was developed as part of a natural language processing coursework study.

## Dataset Structure

The project expects the following structure:

    data/
    ├── raw/
    │   └── column_articles/
    │       ├── author_01/
    │       │   ├── article_01.txt
    │       │   └── ...
    │       ├── author_02/
    │       └── ...
    └── processed/
        ├── column_articles.arff
        └── column_articles.txt

The raw dataset contains:

- 9 authors
- 10 articles per author
- 90 text files in total

## Features

- Turkish text normalization
- stopword removal
- tokenization with Stanza
- lemmatization
- bigram generation
- support for multiple text encodings
- logging results to timestamped output files

## Technologies Used

- Python
- Stanza
- stop-words

## Installation

Clone the repository and install the dependencies:

    pip install -r requirements.txt

## Requirements

The project depends on:

- stanza
- stop-words

## How to Run

Run the script from the project root directory:

    python src/preprocess_turkish_texts.py

## Output

The script:

- loads all documents from the dataset directory
- randomly selects up to 10 documents
- preprocesses them
- writes the results into a timestamped log file under `outputs/`

Example output includes:

- original text preview
- preprocessed text preview
- stopword-removed text preview
- token count
- lemma count
- bigram count
- first tokens, lemmas, and bigrams

## Example Workflow

1. Load article files from `data/raw/column_articles/`
2. Normalize text by lowercasing and removing punctuation
3. Remove Turkish stopwords
4. Apply tokenization and lemmatization with Stanza
5. Extract bigrams
6. Save results to the `outputs/` directory

## Project Structure

    turkish-text-preprocessing-stanza/
    ├── data/
    │   ├── raw/
    │   │   └── column_articles/
    │   └── processed/
    ├── src/
    │   └── preprocess_turkish_texts.py
    ├── outputs/
    ├── requirements.txt
    ├── .gitignore
    └── README.md

## Notes

- The Stanza Turkish model is downloaded automatically on first run.
- Output files are generated automatically and should not be committed to the repository.
- The `outputs/` directory is included in `.gitignore`.

## Future Improvements

- export preprocessing results to CSV or JSON
- add author-level summary statistics
- support configurable sampling size
- add command-line arguments
- improve experiment reproducibility with fixed random seeds
