# Survey Data Visualization

This folder contains four R scripts for exploring and visualizing survey data. The analyses focus on missing data, outliers, categorical distributions, numerical-categorical relationships, and correlation patterns in the presence of missing values.

## Project Overview

The goal of this project is to analyze survey-based data using different visualization techniques and descriptive statistical approaches in R.

The scripts are organized by analysis type so that each one can be run independently.

## Files

- `missing_data_and_outlier_analysis.R`
- `categorical_distribution_visualizations.R`
- `numerical_vs_categorical_visualizations.R`
- `correlation_visualizations_with_missing_data.R`

## Required Input File

Place the following Excel file in the same folder as the scripts:

- `survey_data.xlsx`

## Analysis 1: Missing Data and Outlier Analysis

**File:** `missing_data_and_outlier_analysis.R`

This script examines missing values and outliers in selected numerical variables.

### Method

- loads the dataset from the `Data` sheet
- converts selected columns to numeric format
- creates boxplots for outlier detection
- creates QQ plots for distribution assessment
- visualizes missing value patterns
- generates a missing data heatmap
- saves short textual comments about the findings

### Output

The script creates the folder:

    graph_results/question_1

and saves:

- boxplots for each numerical variable
- QQ plots for each numerical variable
- `missing_data_pattern.png`
- `missing_data_heatmap.png`
- `comments.txt`

## Analysis 2: Categorical Distribution Visualizations

**File:** `categorical_distribution_visualizations.R`

This script visualizes the distribution of selected categorical variables.

### Method

- loads the dataset from the `Data_2` sheet
- converts selected variables to factors
- creates pie charts for category proportions
- creates bar charts for frequency counts
- creates mosaic plots for pairwise relationships between categorical variables
- saves short textual comments for each visualization

### Output

The script creates the folder:

    graph_results/question_2

and saves:

- pie charts
- bar charts
- mosaic plots
- `comments.txt`

## Analysis 3: Numerical vs Categorical Visualizations

**File:** `numerical_vs_categorical_visualizations.R`

This script explores how numerical variables vary across categorical groups.

### Method

- loads the dataset from the `Data_2` sheet
- converts selected numerical columns to numeric type
- converts selected categorical columns to factor type
- creates bar plots with error bars
- creates boxplots
- creates violin plots
- creates point plots with error bars
- saves short textual comments for each comparison

### Output

The script creates the folder:

    graph_results/question_3

and saves:

- bar plots
- boxplots
- violin plots
- point plots
- `comments.txt`

## Analysis 4: Correlation Visualizations with Missing Data

**File:** `correlation_visualizations_with_missing_data.R`

This script analyzes correlations among selected numerical variables while handling missing data.

### Method

- loads the dataset from the `Data` sheet
- converts selected columns to numeric type
- keeps missing values without altering the original data sheet
- computes correlations using `pairwise.complete.obs`
- creates a correlation heatmap
- creates a scatterplot matrix
- creates a correlogram
- creates a correlation network plot
- writes a cleaned version of the data to a new Excel sheet named `Data_Cleaned`

### Output

The script creates the folder:

    graph_results/question_4

and saves:

- `correlation_heatmap.png`
- `scatterplot_matrix.png`
- `correlogram.png`
- `correlation_network_plot.png`
- `comments.txt`

It also updates the Excel file by adding:

- `Data_Cleaned` sheet

## Required Packages

Depending on the script, the following R packages are used:

- `ggplot2`
- `dplyr`
- `readxl`
- `naniar`
- `vcd`
- `corrplot`
- `GGally`
- `openxlsx`
- `rlang`

The scripts install missing packages automatically when needed.

## How to Run

Run each script separately in R:

    source("missing_data_and_outlier_analysis.R")
    source("categorical_distribution_visualizations.R")
    source("numerical_vs_categorical_visualizations.R")
    source("correlation_visualizations_with_missing_data.R")

## Notes

- All scripts expect `survey_data.xlsx` to be in the same folder.
- The scripts use relative paths and automatically create their output folders.
- Missing values marked with `-` in the Excel file are treated as `NA`.
- Each script is independent and can be executed on its own.
