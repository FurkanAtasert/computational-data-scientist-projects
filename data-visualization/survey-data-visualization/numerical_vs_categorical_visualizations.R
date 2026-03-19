packages <- c("ggplot2", "readxl", "dplyr")
installed_packages <- rownames(installed.packages())

for (pkg in packages) {
  if (!(pkg %in% installed_packages)) {
    install.packages(pkg, dependencies = TRUE)
  }
}

library(ggplot2)
library(readxl)
library(dplyr)

# Read the dataset and define '-' values as NA
file_path <- "survey_data.xlsx"

if (!file.exists(file_path)) {
  stop(paste(
    "File not found:",
    file_path,
    "\nMake sure survey_data.xlsx is in the same folder as this script."
  ))
}

df3 <- read_excel(file_path, sheet = "Data_2", na = "-")

# Define column names
numerical_cols <- c("cinsiyet_numerik", "yas_numerik")
categorical_cols <- c(
  "İnternete ne sıklıkla bağlanıyorsunuz",
  "Sosyal medya bağlanma sıklığınız nedir ?"
)

# Check whether the columns exist in the dataset
all_cols <- c(numerical_cols, categorical_cols)
col_exists <- all_cols %in% colnames(df3)
if (!all(col_exists)) {
  missing_cols <- all_cols[!col_exists]
  stop(paste("The following columns were not found in the dataset:", paste(missing_cols, collapse = ", ")))
}

# Convert numerical columns to numeric type
df3[numerical_cols] <- lapply(df3[numerical_cols], as.numeric)

# Convert categorical columns to factor type
df3[categorical_cols] <- lapply(df3[categorical_cols], as.factor)

# Create output folders
if (!dir.exists("graph_results")) {
  dir.create("graph_results")
}
if (!dir.exists("graph_results/question_3")) {
  dir.create("graph_results/question_3")
}

# Vector to store comments
comments_3 <- character()

# Helper function for safe file names
safe_name <- function(x) {
  gsub("[^A-Za-z0-9]+", "_", x)
}

# Function: Create Bar Plot with Error Bars
create_bar_plot <- function(data, numerical_var, categorical_var, folder) {
  summary_df <- data %>%
    group_by(.data[[categorical_var]]) %>%
    summarise(
      mean = mean(.data[[numerical_var]], na.rm = TRUE),
      se = sd(.data[[numerical_var]], na.rm = TRUE) / sqrt(sum(!is.na(.data[[numerical_var]]))),
      .groups = "drop"
    )
  
  p <- ggplot(summary_df, aes(x = .data[[categorical_var]], y = mean, fill = .data[[categorical_var]])) +
    geom_bar(stat = "identity", color = "black", width = 0.7) +
    geom_errorbar(aes(ymin = mean - se, ymax = mean + se), width = 0.2) +
    ggtitle(paste("Mean of", numerical_var, "by", categorical_var)) +
    xlab(categorical_var) +
    ylab(paste("Mean", numerical_var)) +
    theme_minimal() +
    theme(
      legend.position = "none",
      plot.background = element_rect(fill = "white"),
      panel.background = element_rect(fill = "white")
    )
  
  file_name <- paste0(folder, "/barplot_", safe_name(numerical_var), "_by_", safe_name(categorical_var), ".png")
  ggsave(filename = file_name, plot = p, width = 8, height = 6, bg = "white")
  
  highest_group <- summary_df %>% filter(mean == max(mean, na.rm = TRUE))
  comment <- paste(
    "The highest mean value for", numerical_var, "is in the category",
    highest_group[[categorical_var]], "with a value of", round(highest_group$mean, 2), "."
  )
  
  return(comment)
}

# Function: Create Box Plot
create_box_plot <- function(data, numerical_var, categorical_var, folder) {
  p <- ggplot(data, aes(x = .data[[categorical_var]], y = .data[[numerical_var]], fill = .data[[categorical_var]])) +
    geom_boxplot(outlier.color = "red", outlier.shape = 8) +
    ggtitle(paste("Distribution of", numerical_var, "by", categorical_var)) +
    xlab(categorical_var) +
    ylab(numerical_var) +
    theme_minimal() +
    theme(
      legend.position = "none",
      plot.background = element_rect(fill = "white"),
      panel.background = element_rect(fill = "white")
    )
  
  file_name <- paste0(folder, "/boxplot_", safe_name(numerical_var), "_by_", safe_name(categorical_var), ".png")
  ggsave(filename = file_name, plot = p, width = 8, height = 6, bg = "white")
  
  median_df <- data %>%
    group_by(.data[[categorical_var]]) %>%
    summarise(
      median = median(.data[[numerical_var]], na.rm = TRUE),
      .groups = "drop"
    )
  
  highest_group <- median_df %>% filter(median == max(median, na.rm = TRUE))
  comment <- paste(
    "The highest median value for", numerical_var, "is in the category",
    highest_group[[categorical_var]], "with a value of", round(highest_group$median, 2), "."
  )
  
  return(comment)
}

# Function: Create Violin Plot
create_violin_plot <- function(data, numerical_var, categorical_var, folder) {
  p <- ggplot(data, aes(x = .data[[categorical_var]], y = .data[[numerical_var]], fill = .data[[categorical_var]])) +
    geom_violin(trim = FALSE) +
    geom_jitter(width = 0.2, alpha = 0.5, color = "black") +
    ggtitle(paste("Violin Plot of", numerical_var, "by", categorical_var)) +
    xlab(categorical_var) +
    ylab(numerical_var) +
    theme_minimal() +
    theme(
      legend.position = "none",
      plot.background = element_rect(fill = "white"),
      panel.background = element_rect(fill = "white")
    )
  
  file_name <- paste0(folder, "/violinplot_", safe_name(numerical_var), "_by_", safe_name(categorical_var), ".png")
  ggsave(filename = file_name, plot = p, width = 8, height = 6, bg = "white")
  
  mean_df <- data %>%
    group_by(.data[[categorical_var]]) %>%
    summarise(
      mean = mean(.data[[numerical_var]], na.rm = TRUE),
      .groups = "drop"
    )
  
  highest_group <- mean_df %>% filter(mean == max(mean, na.rm = TRUE))
  comment <- paste(
    "The highest mean value for", numerical_var, "is in the category",
    highest_group[[categorical_var]], "with a value of", round(highest_group$mean, 2), "."
  )
  
  return(comment)
}

# Function: Create Point Plot with Error Bars
create_point_plot <- function(data, numerical_var, categorical_var, folder) {
  summary_df <- data %>%
    group_by(.data[[categorical_var]]) %>%
    summarise(
      mean = mean(.data[[numerical_var]], na.rm = TRUE),
      se = sd(.data[[numerical_var]], na.rm = TRUE) / sqrt(sum(!is.na(.data[[numerical_var]]))),
      .groups = "drop"
    )
  
  p <- ggplot(summary_df, aes(x = .data[[categorical_var]], y = mean, group = 1)) +
    geom_point(size = 3, color = "blue") +
    geom_line(color = "blue") +
    geom_errorbar(aes(ymin = mean - se, ymax = mean + se), width = 0.2, color = "blue") +
    ggtitle(paste("Mean of", numerical_var, "by", categorical_var)) +
    xlab(categorical_var) +
    ylab(paste("Mean", numerical_var)) +
    theme_minimal() +
    theme(
      plot.background = element_rect(fill = "white"),
      panel.background = element_rect(fill = "white")
    )
  
  file_name <- paste0(folder, "/pointplot_", safe_name(numerical_var), "_by_", safe_name(categorical_var), ".png")
  ggsave(filename = file_name, plot = p, width = 8, height = 6, bg = "white")
  
  highest_group <- summary_df %>% filter(mean == max(mean, na.rm = TRUE))
  comment <- paste(
    "The highest mean value for", numerical_var, "is in the category",
    highest_group[[categorical_var]], "with a value of", round(highest_group$mean, 2), "."
  )
  
  return(comment)
}

# Create visualizations and collect comments
comments_3 <- c(
  comments_3,
  create_bar_plot(
    df3,
    "cinsiyet_numerik",
    "İnternete ne sıklıkla bağlanıyorsunuz",
    "graph_results/question_3"
  )
)

comments_3 <- c(
  comments_3,
  create_box_plot(
    df3,
    "yas_numerik",
    "İnternete ne sıklıkla bağlanıyorsunuz",
    "graph_results/question_3"
  )
)

comments_3 <- c(
  comments_3,
  create_violin_plot(
    df3,
    "cinsiyet_numerik",
    "Sosyal medya bağlanma sıklığınız nedir ?",
    "graph_results/question_3"
  )
)

comments_3 <- c(
  comments_3,
  create_point_plot(
    df3,
    "yas_numerik",
    "Sosyal medya bağlanma sıklığınız nedir ?",
    "graph_results/question_3"
  )
)

# Save comments
writeLines(comments_3, con = "graph_results/question_3/comments.txt")