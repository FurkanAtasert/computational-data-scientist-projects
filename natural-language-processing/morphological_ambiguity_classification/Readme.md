# Morphological Ambiguity Classification

This project presents a comparative approach to Turkish morphological ambiguity classification using both traditional machine learning and deep learning methods.

The workflow combines TF-IDF features and BERT-based embeddings to represent words, then evaluates two different classifiers:

- Random Forest
- Deep Learning Neural Network

The main goal of the project is to explore how different feature extraction and modeling strategies perform on a Turkish labeled dataset in a multi-class classification setting.

---

## Project Scope

This project focuses on:

- preprocessing a labeled Turkish dataset
- extracting TF-IDF features
- generating BERT-based embeddings
- combining sparse and dense text representations
- training and evaluating multiple classification models
- producing confusion matrices and training curves
- exporting predictions and evaluation results to Excel

---

## Project Structure

morphological-ambiguity-classification/
│
├── artifacts/
│   └── .gitkeep
├── data/
│   ├── test_words.txt
│   ├── turkish_labeled_dataset.txt
│   └── turkish_labeled_dataset.xlsx
├── outputs/
│   └── .gitkeep
├── src/
│   └── morphological_ambiguity_classification.py
├── .gitignore
├── README.md
└── requirements.txt

---

## Methods Used

### Feature Extraction
- TF-IDF vectorization
- BERT embeddings (`dbmdz/bert-base-turkish-cased`)

### Models
- Random Forest with hyperparameter tuning
- Feed-forward deep learning classifier

### Evaluation
- Accuracy
- Classification report
- Confusion matrix
- Training and validation curves

---

## Technologies

- Python
- TensorFlow / Keras
- Hugging Face Transformers
- scikit-learn
- pandas
- NumPy
- matplotlib
- seaborn
- openpyxl

---

## Notes

This project should be interpreted as a structured academic NLP experiment rather than a production-ready language system.

The results may vary depending on:

- class imbalance
- dataset size
- label distribution
- the difficulty of predicting morphological categories from isolated words without broader context

Because the task is performed at the word level, some ambiguity cases may remain difficult to resolve without sentence-level context.

---

## How to Run

### 1. Install dependencies

pip install -r requirements.txt

### 2. Run the project

cd src
python morphological_ambiguity_classification.py

---

## Outputs

After execution, the project generates outputs such as:

- prediction results in Excel format
- confusion matrix visualizations
- deep learning loss curve
- deep learning accuracy curve
- cached vectorizer and embedding artifacts

Generated files are stored in:

- `outputs/`
- `artifacts/`

---

## Limitations

This project has several limitations:

- classification is based on isolated words rather than contextual sequences
- low-frequency classes may reduce model stability
- performance may be limited by dataset quality and label sparsity
- BERT is used as a feature extractor rather than being fully fine-tuned

These limitations are important when interpreting model performance.

---

## Future Improvements

Possible future improvements include:

- adding contextual sentence-based inputs
- comparing with linear models such as Logistic Regression or Linear SVM
- applying direct BERT fine-tuning
- improving label balancing strategies
- adding more detailed experiment tracking and result comparison
