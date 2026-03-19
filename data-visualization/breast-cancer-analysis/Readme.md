# Breast Cancer Analysis in R

This folder contains three R scripts that analyze a breast cancer dataset from different perspectives:

- clustering analysis
- cluster-based ANOVA analysis
- correlation and multiple linear regression analysis

## Project Overview

The goal of this project is to explore breast cancer data using unsupervised learning, group comparison, and regression-based statistical analysis.

The scripts are designed as separate analyses so that each one can be run independently.

## Files

- `breast_cancer_clustering_analysis.R`
- `cluster_based_anova_analysis.R`
- `breast_cancer_correlation_regression_analysis.R`

## Required Input File

Place one of the following Excel files in the same folder as the scripts:

- `breast_cancer_data.xlsx`
- `Breast_Cancer.xlsx`

## Analysis 1: Breast Cancer Clustering Analysis

**File:** `breast_cancer_clustering_analysis.R`

This script applies K-means clustering to the numeric variables in the breast cancer dataset.

### Method

- loads the dataset
- converts `Diagnosis` to a categorical variable
- excludes non-feature columns such as `ID` and `Cluster`
- standardizes numeric variables
- applies K-means clustering with `k = 3`
- adds cluster labels to the dataset
- compares cluster assignments with diagnosis labels

### Output

The script creates the folder:

    results/clustering

and saves:

- `kmeans_clustering_results.png`
- `breast_cancer_with_clusters.csv`
- `kmeans_summary.txt`
- `cluster_diagnosis_table.csv`
- `cluster_vs_diagnosis.png`

## Analysis 2: Cluster-Based ANOVA Analysis

**File:** `cluster_based_anova_analysis.R`

This script performs a one-way ANOVA using cluster membership as the grouping variable and compares the mean values of a selected dependent variable across clusters.

### Method

- loads the dataset
- recreates K-means clusters so the script can run independently
- uses `radius_mean` as the dependent variable
- performs one-way ANOVA
- runs Tukey HSD post hoc analysis
- visualizes the results with boxplots and mean barplots

### Output

The script creates the folder:

    results/anova

and saves:

- `anova_summary.txt`
- `tukey_hsd_result.txt`
- `boxplot_radius_mean.png`
- `mean_values_radius_mean.csv`
- `barplot_mean_radius_mean.png`

## Analysis 3: Correlation and Multiple Linear Regression Analysis

**File:** `breast_cancer_correlation_regression_analysis.R`

This script examines relationships between numeric variables using a correlation matrix and fits a multiple linear regression model.

### Method

- loads the dataset
- selects numeric variables
- computes the correlation matrix
- visualizes the correlation matrix
- uses `radius_mean` as the dependent variable
- fits a multiple linear regression model with the remaining numeric variables
- compares beta coefficients and correlation coefficients

### Output

The script creates the folder:

    results/correlation_regression

and saves:

- `correlation_matrix.png`
- `correlation_matrix.csv`
- `regression_summary.txt`
- `beta_coefficients.png`
- `beta_vs_correlation.png`

## Required Packages

Depending on the script, the following R packages are used:

- `ggplot2`
- `dplyr`
- `cluster`
- `factoextra`
- `ggcorrplot`
- `readxl`

The scripts automatically install missing packages if needed.

## How to Run

Run each script separately in R:

    source("breast_cancer_clustering_analysis.R")
    source("cluster_based_anova_analysis.R")
    source("breast_cancer_correlation_regression_analysis.R")

## Notes

- Each script is independent and can be executed on its own.
- The clustering analysis uses standardized numeric variables.
- The ANOVA and regression analyses both use `radius_mean` as the main dependent variable.
- All results are saved into separate folders under the `results` directory.
