# LSA Topic Modeling

This project demonstrates topic extraction from short Turkish documents using TF-IDF and Latent Semantic Analysis (LSA) with TruncatedSVD.

## Project Overview

The goal of this project is to identify latent topics in a small collection of Turkish text documents.

The workflow includes:

- loading documents from a text file
- preprocessing the text
- removing Turkish stopwords
- converting documents into TF-IDF vectors
- applying TruncatedSVD for LSA
- extracting topic terms
- saving topic outputs and document-topic distributions

This project was developed as part of a natural language processing coursework study.

## Dataset

The project uses a simple text-based dataset:

    data/sample_documents.txt

Each line in the file represents one document.

## Features

- Turkish text preprocessing
- stopword removal with NLTK
- TF-IDF vectorization
- topic modeling with LSA
- topic term extraction
- document-topic distribution export
- automatic result saving with timestamped output folders

## Technologies Used

- Python
- NLTK
- scikit-learn
- pandas
- matplotlib

## Installation

Install the required packages:

    pip install -r requirements.txt

## Requirements

The project depends on:

- numpy
- pandas
- matplotlib
- scikit-learn
- nltk

## How to Run

Run the script from the project root directory:

    python src/lsa_topic_modeling.py

## Output

The script generates a timestamped output directory under:

    outputs/

The output includes:

- topic term text files
- topic term bar charts
- document-topic distribution as CSV

Example generated files:

- `topic_1_terms.txt`
- `topic_1_terms.png`
- `document_topic_distribution.csv`

## Methodology

### 1. Data Loading
Documents are loaded from `data/sample_documents.txt`.

### 2. Preprocessing
Each document is:

- converted to lowercase
- stripped of punctuation
- tokenized
- cleaned from Turkish stopwords

### 3. TF-IDF Representation
The cleaned documents are transformed into a TF-IDF document-term matrix.

### 4. Topic Modeling
TruncatedSVD is applied to the TF-IDF matrix to discover latent topics.

### 5. Result Export
The script saves:

- top terms for each topic
- topic visualizations
- document-topic matrix

## Project Structure

    lsa-topic-modeling-demo/
    ├── data/
    │   └── sample_documents.txt
    ├── src/
    │   └── lsa_topic_modeling.py
    ├── outputs/
    ├── requirements.txt
    ├── .gitignore
    └── README.md

## Notes

- NLTK stopwords are downloaded automatically if not available.
- Output files are generated automatically and should not be committed to the repository.
- The `outputs/` directory should remain in `.gitignore`.

## Future Improvements

- support custom topic counts through command-line arguments
- allow different preprocessing strategies
- add coherence-based topic evaluation
- support larger Turkish corpora
- export results in additional formats such as JSON
