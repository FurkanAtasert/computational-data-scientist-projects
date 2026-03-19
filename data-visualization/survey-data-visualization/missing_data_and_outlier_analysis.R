packages <- c("ggplot2", "naniar", "readxl", "dplyr", "rlang")
installed_packages <- rownames(installed.packages())

for (pkg in packages) {
  if (!(pkg %in% installed_packages)) {
    install.packages(pkg)
  }
}

library(ggplot2)
library(naniar)
library(readxl)
library(dplyr)
library(rlang)

# Read the dataset and define '-' values as NA
file_path <- "survey_data.xlsx"

if (!file.exists(file_path)) {
  stop(paste(
    "File not found:",
    file_path,
    "\nMake sure survey_data.xlsx is in the same folder as this script."
  ))
}

df <- read_excel(file_path, sheet = "Data", na = "-")

# Define column names
cols <- c(
  "Ages 15-19,Male", "Ages 15-19,Female",
  "Ages 20-24,Male", "Ages 20-24,Female",
  "Ages 25-29,Male", "Ages 25-29,Female",
  "Ages 30-34,Male", "Ages 30-34,Female",
  "Ages 35-39,Male", "Ages 35-39,Female"
)

# Check whether the columns exist in the dataset
col_exists <- cols %in% colnames(df)
if (!all(col_exists)) {
  missing_cols <- cols[!col_exists]
  stop(paste("The following columns were not found in the dataset:", paste(missing_cols, collapse = ", ")))
}

# Convert columns to numeric type
df[cols] <- lapply(df[cols], as.numeric)

# Create output folders
if (!dir.exists("graph_results")) {
  dir.create("graph_results")
}
if (!dir.exists("graph_results/question_1")) {
  dir.create("graph_results/question_1")
}

# Vector to store comments
comments <- character()

# Helper function for safe file names
safe_name <- function(x) {
  gsub("[^A-Za-z0-9]+", "_", x)
}

# Outlier analysis and visualization
for (col in cols) {
  if (is.numeric(df[[col]])) {
    # Boxplot
    p_box <- ggplot(df, aes(y = .data[[col]])) +
      geom_boxplot(fill = "lightblue", outlier.color = "red", outlier.shape = 8) +
      ggtitle(paste(col, "Outlier Analysis")) +
      xlab("") +
      ylab(col) +
      theme_bw() +
      theme(
        plot.background = element_rect(fill = "white"),
        panel.background = element_rect(fill = "white")
      )
    
    file_name_box <- paste0("graph_results/question_1/boxplot_", safe_name(col), ".png")
    ggsave(filename = file_name_box, plot = p_box, width = 8, height = 6, bg = "white")
    
    # QQ Plot
    p_qq <- ggplot(df, aes(sample = .data[[col]])) +
      stat_qq(color = "blue", na.rm = TRUE) +
      stat_qq_line(color = "red", na.rm = TRUE) +
      ggtitle(paste(col, "QQ Plot")) +
      xlab("Theoretical Quantiles") +
      ylab("Sample Quantiles") +
      theme_bw() +
      theme(
        plot.background = element_rect(fill = "white"),
        panel.background = element_rect(fill = "white")
      )
    
    file_name_qq <- paste0("graph_results/question_1/qqplot_", safe_name(col), ".png")
    ggsave(filename = file_name_qq, plot = p_qq, width = 8, height = 6, bg = "white")
    
    # Outlier analysis
    data_col <- na.omit(df[[col]])
    outliers <- boxplot.stats(data_col)$out
    n_outliers <- length(outliers)
    
    comment <- paste("The variable", col, "contains", n_outliers, "outlier(s).")
    comments <- c(comments, comment)
  } else {
    comment <- paste("The variable", col, "was not analyzed because it is not numeric.")
    comments <- c(comments, comment)
  }
}

# Missing data analysis and visualization
p_miss <- gg_miss_var(df[cols]) +
  ggtitle("Missing Data Pattern") +
  xlab("Variables") +
  ylab("Number of Missing Values") +
  theme_bw() +
  theme(
    plot.background = element_rect(fill = "white"),
    panel.background = element_rect(fill = "white")
  )

ggsave(
  filename = "graph_results/question_1/missing_data_pattern.png",
  plot = p_miss,
  width = 8,
  height = 6,
  bg = "white"
)

# Calculate missing value counts
missing_counts <- sapply(df[cols], function(x) sum(is.na(x)))

# Add missing data comments
for (col in cols) {
  n_missing <- missing_counts[[col]]
  comment <- paste("The variable", col, "contains", n_missing, "missing value(s).")
  comments <- c(comments, comment)
}

# Missing data heatmap
p_miss_heatmap <- vis_miss(df[cols]) +
  ggtitle("Missing Data Heatmap") +
  theme_bw() +
  theme(
    plot.background = element_rect(fill = "white"),
    panel.background = element_rect(fill = "white")
  )

ggsave(
  filename = "graph_results/question_1/missing_data_heatmap.png",
  plot = p_miss_heatmap,
  width = 8,
  height = 6,
  bg = "white"
)

comment <- "Missing Data Heatmap: This plot visualizes the distribution of missing values in the dataset. Each cell shows whether a specific variable contains a missing value for a given observation."
comments <- c(comments, comment)

writeLines(comments, con = "graph_results/question_1/comments.txt")