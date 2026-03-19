packages <- c("ggplot2", "readxl", "dplyr", "corrplot", "GGally", "openxlsx")
installed_packages <- rownames(installed.packages())

for (pkg in packages) {
  if (!(pkg %in% installed_packages)) {
    install.packages(pkg, dependencies = TRUE)
  }
}

library(ggplot2)
library(readxl)
library(dplyr)
library(corrplot)
library(GGally)
library(openxlsx)

# Read the dataset and define '-' values as NA
file_path <- "survey_data.xlsx"

if (!file.exists(file_path)) {
  stop(paste(
    "File not found:",
    file_path,
    "\nMake sure survey_data.xlsx is in the same folder as this script."
  ))
}

df_original <- read_excel(file_path, sheet = "Data", na = "-")

# Define column names
numerical_cols <- c(
  "Ages 15-19,Male", "Ages 15-19,Female",
  "Ages 20-24,Male", "Ages 20-24,Female",
  "Ages 25-29,Male", "Ages 25-29,Female",
  "Ages 30-34,Male", "Ages 30-34,Female",
  "Ages 35-39,Male", "Ages 35-39,Female"
)

# Check whether the columns exist in the dataset
col_exists <- numerical_cols %in% colnames(df_original)
if (!all(col_exists)) {
  missing_cols <- numerical_cols[!col_exists]
  stop(paste("The following columns were not found in the dataset:", paste(missing_cols, collapse = ", ")))
}

# Create a cleaned copy without modifying the original dataset
df_clean <- df_original

# Convert numerical columns to numeric type
df_clean[numerical_cols] <- lapply(df_clean[numerical_cols], function(x) as.numeric(x))

# Create output folders
if (!dir.exists("graph_results")) {
  dir.create("graph_results")
}
if (!dir.exists("graph_results/question_4")) {
  dir.create("graph_results/question_4")
}

# Vector to store comments
comments_4 <- character()

# Function: Create Correlation Heatmap
create_corr_heatmap <- function(data, cols, folder) {
  corr_matrix <- cor(data[, cols], use = "pairwise.complete.obs", method = "pearson")
  
  png(filename = paste0(folder, "/correlation_heatmap.png"), width = 800, height = 600, bg = "white")
  corrplot(
    corr_matrix,
    method = "color",
    type = "upper",
    addCoef.col = "black",
    tl.col = "black",
    tl.srt = 45,
    diag = FALSE
  )
  dev.off()
  
  comment <- "Correlation Heatmap: Correlations between columns are shown using color intensity. Red indicates strong positive correlation, while blue indicates strong negative correlation."
  return(comment)
}

# Function: Create Scatterplot Matrix
create_scatterplot_matrix <- function(data, cols, folder) {
  p <- ggpairs(
    data[, cols],
    upper = list(continuous = wrap("cor", size = 3)),
    lower = list(continuous = "points"),
    diag = list(continuous = "densityDiag")
  ) +
    theme(
      panel.background = element_rect(fill = "white"),
      plot.background = element_rect(fill = "white")
    )
  
  ggsave(filename = paste0(folder, "/scatterplot_matrix.png"), plot = p, width = 12, height = 10, bg = "white")
  
  comment <- "Scatterplot Matrix: Relationships between columns are displayed using pairwise scatterplots. The upper panels include correlation coefficients."
  return(comment)
}

# Function: Create Correlogram
create_correlogram <- function(data, cols, folder) {
  corr_matrix <- cor(data[, cols], use = "pairwise.complete.obs", method = "pearson")
  
  png(filename = paste0(folder, "/correlogram.png"), width = 800, height = 800, bg = "white")
  corrplot(
    corr_matrix,
    method = "circle",
    type = "full",
    addCoef.col = "black",
    tl.col = "black",
    tl.srt = 45,
    diag = FALSE
  )
  dev.off()
  
  comment <- "Correlogram: Correlations between columns are displayed using circles. The size and color of the circles represent the strength and direction of the correlation."
  return(comment)
}

# Function: Create Network Plot
create_network_plot <- function(data, cols, folder) {
  corr_matrix <- cor(data[, cols], use = "pairwise.complete.obs", method = "pearson")
  
  corr_long <- as.data.frame(as.table(corr_matrix))
  corr_long <- corr_long[corr_long$Var1 != corr_long$Var2, ]
  
  # Filter stronger relationships for the network plot (|r| > 0.5)
  corr_long_filtered <- corr_long %>% filter(abs(Freq) > 0.5)
  
  p <- ggplot(corr_long_filtered, aes(x = Var1, y = Var2, size = abs(Freq), color = Freq)) +
    geom_point(alpha = 0.7) +
    geom_text(aes(label = round(Freq, 2)), vjust = 1.5, size = 3) +
    scale_color_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0) +
    theme_minimal() +
    theme(
      axis.text.x = element_text(angle = 45, hjust = 1, color = "black"),
      axis.text.y = element_text(color = "black"),
      plot.background = element_rect(fill = "white"),
      panel.background = element_rect(fill = "white")
    ) +
    ggtitle("Correlation Network Plot") +
    xlab("") +
    ylab("")
  
  ggsave(filename = paste0(folder, "/correlation_network_plot.png"), plot = p, width = 8, height = 6, bg = "white")
  
  comment <- "Correlation Network Plot: Highly correlated relationships between columns are displayed as a network. Red indicates positive correlation, while blue indicates negative correlation."
  return(comment)
}

# Generate visualizations and collect comments
comments_4 <- c(comments_4, create_corr_heatmap(df_clean, numerical_cols, "graph_results/question_4"))
comments_4 <- c(comments_4, create_scatterplot_matrix(df_clean, numerical_cols, "graph_results/question_4"))
comments_4 <- c(comments_4, create_correlogram(df_clean, numerical_cols, "graph_results/question_4"))
comments_4 <- c(comments_4, create_network_plot(df_clean, numerical_cols, "graph_results/question_4"))

# Save comments
writeLines(comments_4, con = "graph_results/question_4/comments.txt")

# Write the cleaned data into the Excel file as a new sheet without modifying the original data sheet
wb <- loadWorkbook(file_path)
if (!"Data_Cleaned" %in% names(wb)) {
  addWorksheet(wb, "Data_Cleaned")
  writeData(wb, sheet = "Data_Cleaned", df_clean)
  saveWorkbook(wb, file_path, overwrite = TRUE)
  message("Cleaned data was successfully added to the 'Data_Cleaned' sheet.")
} else {
  message("The 'Data_Cleaned' sheet already exists. Cleaned data was not added.")
}