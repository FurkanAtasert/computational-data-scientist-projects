install.packages("readxl")
install.packages("ggplot2")

library(readxl)
library(ggplot2)

data <- read_excel("hematology_bar_charts.xlsx")

# Specified column names
selected_columns <- c("MPV", "Lenf", "Monosit")

# Function to remove empty columns
empty_columns <- colnames(data)[sapply(data, function(x) all(is.na(x) | x == ""))]
clean_data <- data[, !colnames(data) %in% empty_columns]

# Define a function to create bar plots
create_bar_plot <- function(data, column_name, file_name) {
  plot <- ggplot(data = data, aes(x = get(column_name))) +
    geom_bar(fill = "blue") +
    labs(title = paste(column_name, "Bar Plot"), x = column_name, y = "Count") +
    theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1))
  
  # Save the plot to a file
  png(filename = paste(file_name, "_bar.png", sep = ""))
  print(plot)
  dev.off()
}

# Create and save bar plots for the specified columns
for (column_name in selected_columns) {
  create_bar_plot(clean_data, column_name, paste(column_name, "_bar", sep = ""))
}