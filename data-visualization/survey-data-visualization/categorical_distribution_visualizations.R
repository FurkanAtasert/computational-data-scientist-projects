packages <- c("ggplot2", "naniar", "readxl", "dplyr", "vcd")
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
library(vcd)

# Read the Excel file and define '-' values as NA
file_path <- "survey_data.xlsx"

if (!file.exists(file_path)) {
  stop(paste(
    "File not found:",
    file_path,
    "\nMake sure survey_data.xlsx is in the same folder as this script."
  ))
}

df2 <- read_excel(file_path, sheet = "Data_2", na = "-")

# Define categorical columns
# Original dataset column names are preserved
categorical_cols <- c(
  "yas",
  "İnternete ne sıklıkla bağlanıyorsunuz",
  "Sosyal medya bağlanma sıklığınız nedir ?"
)

# Check whether the columns exist in the dataset
col_exists <- categorical_cols %in% colnames(df2)
if (!all(col_exists)) {
  missing_cols <- categorical_cols[!col_exists]
  stop(paste(
    "The following columns were not found in the dataset:",
    paste(missing_cols, collapse = ", ")
  ))
}

# Convert categorical columns to factor type
df2[categorical_cols] <- lapply(df2[categorical_cols], as.factor)

# Create output folders
if (!dir.exists("graph_results")) {
  dir.create("graph_results")
}
if (!dir.exists("graph_results/question_2")) {
  dir.create("graph_results/question_2")
}

# Vector to store comments
comments_2 <- character()

# Function: Create Pie Chart
create_pie_chart <- function(data, column, folder) {
  pie_data <- data %>%
    group_by(!!sym(column)) %>%
    summarise(Frequency = n(), .groups = "drop") %>%
    mutate(
      Percentage = Frequency / sum(Frequency) * 100,
      Label = paste0(round(Percentage, 1), "%")
    )
  
  p <- ggplot(pie_data, aes(x = "", y = Frequency, fill = !!sym(column))) +
    geom_bar(stat = "identity", width = 1, color = "white") +
    coord_polar(theta = "y") +
    geom_text(aes(label = Label), position = position_stack(vjust = 0.5)) +
    ggtitle(paste(column, "Pie Chart")) +
    theme_void() +
    theme(
      legend.title = element_blank(),
      plot.background = element_rect(fill = "white"),
      panel.background = element_rect(fill = "white")
    )
  
  file_name <- paste0(folder, "/pie_", gsub("[ /,?]", "_", column), ".png")
  ggsave(filename = file_name, plot = p, width = 8, height = 6, bg = "white")
  
  most_common <- pie_data %>% filter(Frequency == max(Frequency))
  comment <- paste(
    "Most common category in", column, ":",
    as.character(most_common[[column]]),
    "(", most_common$Frequency, "observations,",
    round(most_common$Percentage, 1), "%)", sep = " "
  )
  
  return(comment)
}

# Function: Create Bar Chart
create_bar_chart <- function(data, column, folder) {
  p <- ggplot(data, aes(x = !!sym(column), fill = !!sym(column))) +
    geom_bar(color = "black") +
    geom_text(stat = "count", aes(label = after_stat(count)), vjust = -0.5) +
    ggtitle(paste(column, "Bar Chart")) +
    xlab(column) +
    ylab("Frequency") +
    theme_minimal() +
    theme(
      legend.position = "none",
      plot.background = element_rect(fill = "white"),
      panel.background = element_rect(fill = "white")
    )
  
  file_name <- paste0(folder, "/bar_", gsub("[ /,?]", "_", column), ".png")
  ggsave(filename = file_name, plot = p, width = 8, height = 6, bg = "white")
  
  most_common <- data %>%
    group_by(!!sym(column)) %>%
    summarise(Frequency = n(), .groups = "drop") %>%
    arrange(desc(Frequency)) %>%
    slice(1)
  
  comment <- paste(
    "Most common category in", column, ":",
    as.character(most_common[[column]]),
    "(", most_common$Frequency, "observations)", sep = " "
  )
  
  return(comment)
}

# Function: Create Mosaic Plot
create_mosaic_plot <- function(data, columns_pair, folder) {
  if (length(columns_pair) != 2) {
    stop("Two variables are required for a mosaic plot.")
  }
  
  tab <- table(data[[columns_pair[1]]], data[[columns_pair[2]]])
  mosaic_name <- paste0(
    folder, "/mosaic_",
    paste(gsub("[ /,?]", "_", columns_pair), collapse = "_vs_"),
    ".png"
  )
  
  png(filename = mosaic_name, width = 800, height = 600, bg = "white")
  tryCatch({
    mosaic(
      tab,
      shade = TRUE,
      legend = TRUE,
      main = paste("Mosaic Plot:", paste(columns_pair, collapse = " vs "))
    )
  }, error = function(e) {
    message(paste("Error while creating mosaic plot:", e$message))
  })
  dev.off()
  
  comment <- paste(
    "The mosaic plot suggests a relationship between",
    columns_pair[1], "and", columns_pair[2], "."
  )
  
  return(comment)
}

# Create pie charts and bar charts for categorical variables
for (col in categorical_cols) {
  comment_pie <- create_pie_chart(df2, col, "graph_results/question_2")
  comments_2 <- c(comments_2, comment_pie)
  
  comment_bar <- create_bar_chart(df2, col, "graph_results/question_2")
  comments_2 <- c(comments_2, comment_bar)
}

# Create mosaic plots for all pairwise combinations
combinations <- combn(categorical_cols, 2, simplify = FALSE)
for (pair in combinations) {
  comment_mosaic <- create_mosaic_plot(df2, pair, "graph_results/question_2")
  comments_2 <- c(comments_2, comment_mosaic)
}

writeLines(comments_2, con = "graph_results/question_2/comments.txt")