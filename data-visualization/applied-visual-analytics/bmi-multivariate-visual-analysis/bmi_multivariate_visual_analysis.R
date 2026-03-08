# Install required packages
install.packages("readxl")    # For reading Excel files
install.packages("writexl")   # For writing Excel files
install.packages("ggplot2")   # For plotting
install.packages("corrplot")  # For correlation matrix visualization
install.packages("GGally")    # For pair plots
install.packages("reshape2")  # For heatmap preparation
install.packages("cowplot")   # For plot arrangement
library(readxl)
library(writexl)
library(ggplot2)
library(corrplot)
library(GGally)
library(reshape2)
library(cowplot)

# Read the Excel file
data <- read_excel("bmi_dataset.xlsx")

# Select numeric variables
numeric_data <- data[, sapply(data, is.numeric)]

# Clean the data by removing missing values
clean_data <- na.omit(numeric_data)

# Normality tests
normality_tests <- sapply(names(clean_data), function(col) {
  test_result <- tryCatch({
    shapiro.test(clean_data[[col]])$p.value
  }, error = function(e) NA)  # Return NA in case of error
  return(test_result)
})

# Print p-values for each variable
print(normality_tests)

# Determine whether each variable follows a normal distribution
normality_results <- sapply(normality_tests, function(p) p > 0.05)
normality_summary <- data.frame(
  Column = names(normality_results),
  P_Value = normality_tests,
  Normal_Distribution = ifelse(normality_results, "Yes", "No")
)
write_xlsx(normality_summary, "bmi_normality_summary.xlsx")
print(normality_summary)

# Compute the correlation matrix
correlation_matrix_original <- cor(clean_data, use = "complete.obs")

# Create a data frame for the correlation matrix
correlation_matrix_df <- as.data.frame(correlation_matrix_original)

# Save plots as JPEG files

# 1. Correlation Matrix Plot (Original Data)
jpeg("correlation_matrix_original.jpg", width = 1200, height = 1200)
corrplot(
  correlation_matrix_original,
  method = "color",
  addCoef.col = "black",
  tl.cex = 0.8,
  title = "Correlation Matrix (Original Data)",
  mar = c(1, 1, 2, 1),  # Adjust plot margins
  tl.col = "black"      # Set label color
)
dev.off()

# 2. Pair Plot
jpeg("pairs_plot.jpg", width = 1600, height = 1600)
print(
  ggpairs(
    clean_data,
    title = "Pair Plot",
    upper = list(continuous = wrap("cor", size = 5, color = "blue")),
    lower = list(continuous = wrap("smooth", size = 1, color = "blue")),
    diag = list(continuous = wrap("barDiag", size = 1, fill = "lightblue"))
  )
)
dev.off()

# 3. Scatter Plot Matrix
jpeg("scatter_plot_matrix.jpg", width = 1600, height = 1600)
pairs(
  clean_data,
  main = "Scatter Plot Matrix",
  pch = 16,
  col = "blue",
  cex = 0.5,
  labels = colnames(clean_data)
)
dev.off()

# 4. Heatmap
heatmap_data <- melt(correlation_matrix_original)
jpeg("heatmap.jpg", width = 1200, height = 1200)
print(
  ggplot(heatmap_data, aes(Var1, Var2, fill = value)) +
    geom_tile() +
    scale_fill_gradient2(
      low = "blue",
      high = "red",
      mid = "white",
      midpoint = 0,
      limit = c(-1, 1)
    ) +
    theme_minimal() +
    labs(
      title = "Correlation Heatmap",
      x = "Variables",
      y = "Variables",
      fill = "Correlation"
    ) +
    theme(
      axis.text.x = element_text(angle = 45, hjust = 1, size = 10),
      axis.text.y = element_text(size = 10),
      title = element_text(size = 15)
    )
)
dev.off()

# 5. Correlation Distribution Plot
correlation_values <- as.vector(correlation_matrix_original)
jpeg("correlation_distribution.jpg", width = 1200, height = 800)
print(
  ggplot(data.frame(correlation = correlation_values), aes(x = correlation)) +
    geom_histogram(bins = 30, fill = "steelblue", color = "black", alpha = 0.7) +
    labs(
      title = "Correlation Distribution Plot",
      x = "Correlation Coefficients",
      y = "Frequency"
    ) +
    theme_minimal() +
    theme(
      title = element_text(size = 15),
      axis.text = element_text(size = 12),
      axis.title = element_text(size = 14),
      plot.margin = margin(10, 10, 10, 10)
    )
)
dev.off()

# 6. Bubble Plot (using the first four variables as an example)
jpeg("bubble_plot.jpg", width = 1200, height = 1200)
print(
  ggplot(
    clean_data,
    aes(
      x = clean_data[[1]],
      y = clean_data[[2]],
      size = clean_data[[3]],
      color = clean_data[[4]]
    )
  ) +
    geom_point(alpha = 0.7) +
    scale_size_continuous(range = c(2, 15)) +
    labs(
      title = "Bubble Plot",
      x = names(clean_data)[1],
      y = names(clean_data)[2],
      size = "Third Variable",
      color = "Fourth Variable"
    ) +
    theme_minimal() +
    theme(
      title = element_text(size = 15),
      axis.text = element_text(size = 12)
    )
)
dev.off()

# 7. QQ Plot (for each variable)
jpeg("qq_plot.jpg", width = 1600, height = 1600)
par(mfrow = c(ceiling(sqrt(ncol(clean_data))), ceiling(sqrt(ncol(clean_data)))))  # Multi-plot layout
for (col in names(clean_data)) {
  qqnorm(
    clean_data[[col]],
    main = paste("QQ Plot -", col),
    xlab = "Theoretical Quantiles",
    ylab = "Sample Quantiles",
    col = "blue",
    pch = 16
  )
  qqline(clean_data[[col]], col = "red")
}
dev.off()

# 8. Normal Distribution Plot (for each variable)
jpeg("normal_distribution.jpg", width = 1600, height = 1600)
par(mfrow = c(ceiling(sqrt(ncol(clean_data))), ceiling(sqrt(ncol(clean_data)))))  # Multi-plot layout
for (col in names(clean_data)) {
  hist(
    clean_data[[col]],
    breaks = 30,
    probability = TRUE,
    main = paste("Normal Distribution -", col),
    xlab = col,
    ylab = "Density",
    col = "lightblue",
    border = "black"
  )
  curve(
    dnorm(x, mean = mean(clean_data[[col]]), sd = sd(clean_data[[col]])),
    add = TRUE,
    col = "red",
    lwd = 2
  )
}
dev.off()

# 9. Boxplot (for each variable)
jpeg("boxplot.jpg", width = 1600, height = 1600)
par(mfrow = c(ceiling(sqrt(ncol(clean_data))), ceiling(sqrt(ncol(clean_data)))))  # Multi-plot layout
for (col in names(clean_data)) {
  boxplot(
    clean_data[[col]],
    main = paste("Boxplot -", col),
    ylab = col,
    col = "lightblue",
    border = "black"
  )
}
dev.off()