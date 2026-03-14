# Country Similarity Analysis with a Vector Space Model

This project compares countries using a vector space model built from selected World Bank economic indicators.  
It measures similarity between countries using Euclidean distance and cosine distance.

## Project Overview

The goal of this project is to represent each country as a numerical vector based on economic indicators and compare countries in terms of similarity.

The workflow includes:

- downloading country-level data from the World Bank
- filtering out aggregate regions
- building vector representations for countries
- selecting a target country
- computing Euclidean and cosine distances
- identifying the most similar countries

This project was developed as part of a computational statistics coursework study.

## Data Source

The data is retrieved from the World Bank using `pandas-datareader`.

Indicators used in the analysis:

- exports
- imports
- agriculture value added
- GDP
- external balance on goods and services

The default analysis year is:

- 2010

The default target country is:

- Australia

## Features

- automatic World Bank data retrieval
- filtering of aggregate regions
- country vector construction
- similarity analysis with Euclidean distance
- similarity analysis with cosine distance
- readable tabular output

## Technologies Used

- Python
- pandas
- numpy
- pandas-datareader

## Installation

Install the required packages:

    pip install -r requirements.txt

## Requirements

The project depends on:

- pandas
- numpy
- pandas-datareader

## How to Run

Run the script from the project root directory:

    python src/country_similarity_analysis.py

## Output

The script prints:

- target country
- analysis year
- number of countries analyzed
- countries closest to the target country by Euclidean distance
- countries closest to the target country by cosine distance
- selected country details for comparison

## Methodology

### 1. Data Collection
Country-level economic data is downloaded from the World Bank API.

### 2. Filtering
Aggregate entries such as regional and income-level summaries are removed.

### 3. Vector Representation
Each country is represented as a vector of selected indicator values.

### 4. Similarity Computation
Two distance metrics are used:

- **Euclidean distance** for direct geometric distance
- **Cosine distance** for orientation-based similarity

## Project Structure

    country_similarity_analysis/
    ├── src/
    │   └── country_similarity_analysis.py
    ├── reports/
    │   └── vector-space-model-report.docx
    ├── requirements.txt
    ├── .gitignore
    └── README.md

## Example Use Case

This project can be used to explore questions such as:

- Which countries are economically similar to Australia?
- Do Euclidean and cosine distance produce similar rankings?
- How do selected economic indicators affect similarity patterns?

## Future Improvements

- allow the target country to be passed as a command-line argument
- support multiple years
- normalize indicators before comparison
- add visualizations for country similarity
- export results to CSV
- compare ranking stability across distance metrics

## Notes

- Results may vary depending on data availability for specific countries and indicators.
- Missing values are removed before similarity computation.
- Similarity depends strongly on the selected indicators and year.
