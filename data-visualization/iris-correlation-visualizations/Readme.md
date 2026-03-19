# Iris Correlation Visualizations

This project explores relationships between variables in the built-in `iris` dataset using correlation analysis and multiple visualization techniques in R.

## Project Overview

The goal of this analysis is to examine numerical and categorical relationships in the `iris` dataset and present them with clear visualizations.

The script includes:

- normality testing for numerical variables
- correlation analysis between numerical variables
- eta squared analysis between categorical and numerical variables
- correlation-based visualizations

## File

- `iris_correlation_visualizations.R`

## Dataset

This project uses the built-in R dataset:

- `iris`

No external data file is required.

## Method

The analysis follows these steps:

1. Load the `iris` dataset.
2. Inspect the structure and summary of the dataset.
3. Define numerical and categorical variables.
4. Apply the Shapiro-Wilk normality test to numerical variables.
5. Choose Pearson or Spearman correlation depending on the normality results.
6. Compute eta squared values for categorical-numerical relationships.
7. Generate multiple visualizations for the numerical correlation structure.

## Visualizations

The script creates the following visual outputs:

- correlation heatmap
- scatterplot matrix
- correlogram
- correlation network plot

## Output Files

The script saves the following files:

- `correlation_heatmap.png`
- `scatterplot_matrix.png`
- `correlogram.png`
- `correlation_network_plot.png`

## Required Packages

The script uses the following R packages:

- `ggplot2`
- `dplyr`
- `corrplot`
- `GGally`
- `DescTools`

If any package is missing, the script asks you to install it before running.

## How to Run

Run the script in R:

    source("iris_correlation_visualizations.R")

## Notes

- The project uses the built-in `iris` dataset, so no Excel or CSV file is needed.
- Pearson correlation is used when both variables satisfy the normality condition.
- Spearman correlation is used when the normality condition is not met.
- Eta squared is used to measure the relationship between the categorical variable and numerical variables.
