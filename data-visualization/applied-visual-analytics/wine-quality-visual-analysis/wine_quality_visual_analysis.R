# Install required packages
install.packages("readxl")
install.packages("ggplot2")
install.packages("dplyr")
install.packages("outliers")
install.packages("car")
install.packages("writexl")

library(readxl)
library(ggplot2)
library(dplyr)
library(outliers)
library(car)
library(writexl)

# Read the dataset
file_path <- "wine_quality.xlsx"
data <- read_excel(file_path)

# Clean column names
names(data) <- gsub(",", "", names(data))
print(names(data))

# Check missing values in the dataset
missing_values <- sum(is.na(data))
cat("There are", missing_values, "missing values in the dataset.\n")

# Check which columns contain missing values
missing_summary <- colSums(is.na(data))
print(missing_summary)

# Fill missing values with the median
data$alcohol[is.na(data$alcohol)] <- median(data$alcohol, na.rm = TRUE)

# Check missing values after handling them
missing_values_post <- sum(is.na(data))
cat("After handling missing values, there are", missing_values_post, "missing values in the dataset.\n")

# Define plot settings
theme_settings <- theme(
  panel.background = element_rect(fill = "white", colour = "black"),
  panel.grid.major = element_line(colour = "grey80"),
  panel.grid.minor = element_line(colour = "grey90"),
  plot.background = element_rect(fill = "white", colour = NA),
  axis.text = element_text(size = 12),
  axis.title = element_text(size = 14),
  title = element_text(size = 16)
)

# Boxplot: Acidity by Quality
boxplot_acidity_quality <- ggplot(data, aes(x = as.factor(quality), y = acidity, fill = as.factor(quality))) + 
  geom_boxplot(outlier.colour = "red", outlier.shape = 16) +
  labs(title = "Boxplot of Acidity by Quality", x = "Quality", y = "Acidity") +
  theme_minimal() +
  theme_settings
ggsave("boxplot_acidity_quality.png", plot = boxplot_acidity_quality, width = 10, height = 6)

# Boxplot: Alcohol by Quality
boxplot_alcohol_quality <- ggplot(data, aes(x = as.factor(quality), y = alcohol, fill = as.factor(quality))) + 
  geom_boxplot(outlier.colour = "red", outlier.shape = 16) +
  labs(title = "Boxplot of Alcohol by Quality", x = "Quality", y = "Alcohol") +
  theme_minimal() +
  theme_settings
ggsave("boxplot_alcohol_quality.png", plot = boxplot_alcohol_quality, width = 10, height = 6)

# Violin Plot: Acidity by Quality
violin_acidity_quality <- ggplot(data, aes(x = as.factor(quality), y = acidity, fill = as.factor(quality))) + 
  geom_violin(alpha = 0.5) +
  labs(title = "Violin Plot of Acidity by Quality", x = "Quality", y = "Acidity") +
  theme_minimal() +
  theme_settings
ggsave("violin_acidity_quality.png", plot = violin_acidity_quality, width = 10, height = 6)

# Violin Plot: Alcohol by Quality
violin_alcohol_quality <- ggplot(data, aes(x = as.factor(quality), y = alcohol, fill = as.factor(quality))) + 
  geom_violin(alpha = 0.5) +
  labs(title = "Violin Plot of Alcohol by Quality", x = "Quality", y = "Alcohol") +
  theme_minimal() +
  theme_settings
ggsave("violin_alcohol_quality.png", plot = violin_alcohol_quality, width = 10, height = 6)

# Density Plot: Acidity by Quality
density_acidity_quality <- ggplot(data, aes(x = acidity, fill = as.factor(quality))) + 
  geom_density(alpha = 0.5) +
  labs(title = "Density Distribution of Acidity by Quality", x = "Acidity", y = "Density") +
  theme_minimal() +
  theme_settings
ggsave("density_acidity_quality.png", plot = density_acidity_quality, width = 10, height = 6)

# Density Plot: Alcohol by Quality
density_alcohol_quality <- ggplot(data, aes(x = alcohol, fill = as.factor(quality))) + 
  geom_density(alpha = 0.5) +
  labs(title = "Density Distribution of Alcohol by Quality", x = "Alcohol", y = "Density") +
  theme_minimal() +
  theme_settings
ggsave("density_alcohol_quality.png", plot = density_alcohol_quality, width = 10, height = 6)

# Line Plot: Acidity by Quality
line_acidity_quality <- ggplot(data, aes(x = as.factor(quality), y = acidity, group = 1)) + 
  geom_line(color = "blue") +
  geom_point(color = "red") +
  labs(title = "Line Plot of Acidity by Quality", x = "Quality", y = "Acidity") +
  theme_minimal() +
  theme_settings
ggsave("line_acidity_quality.png", plot = line_acidity_quality, width = 10, height = 6)

# Line Plot: Alcohol by Quality
line_alcohol_quality <- ggplot(data, aes(x = as.factor(quality), y = alcohol, group = 1)) + 
  geom_line(color = "blue") +
  geom_point(color = "red") +
  labs(title = "Line Plot of Alcohol by Quality", x = "Quality", y = "Alcohol") +
  theme_minimal() +
  theme_settings
ggsave("line_alcohol_quality.png", plot = line_alcohol_quality, width = 10, height = 6)

# Histogram: Acidity by Quality
histogram_acidity_quality <- ggplot(data, aes(x = acidity, fill = as.factor(quality))) + 
  geom_histogram(binwidth = 0.5, position = "dodge", alpha = 0.7) +
  labs(title = "Histogram of Acidity by Quality", x = "Acidity", y = "Frequency") +
  theme_minimal() +
  theme_settings
ggsave("histogram_acidity_quality.png", plot = histogram_acidity_quality, width = 10, height = 6)

# Histogram: Alcohol by Quality
histogram_alcohol_quality <- ggplot(data, aes(x = alcohol, fill = as.factor(quality))) + 
  geom_histogram(binwidth = 0.5, position = "dodge", alpha = 0.7) +
  labs(title = "Histogram of Alcohol by Quality", x = "Alcohol", y = "Frequency") +
  theme_minimal() +
  theme_settings
ggsave("histogram_alcohol_quality.png", plot = histogram_alcohol_quality, width = 10, height = 6)

# Standard Normal Distribution Plot: Acidity
standard_normal_acidity <- ggplot(data, aes(x = acidity)) +
  geom_density(aes(y = ..density..), fill = "blue", alpha = 0.5) +
  stat_function(fun = dnorm, args = list(mean = mean(data$acidity, na.rm = TRUE), sd = sd(data$acidity, na.rm = TRUE)), color = "red", size = 1) +
  labs(title = "Standard Normal Distribution Plot for Acidity", x = "Acidity", y = "Density") +
  theme_minimal() +
  theme_settings
ggsave("standard_normal_acidity.png", plot = standard_normal_acidity, width = 10, height = 6)

# Standard Normal Distribution Plot: Alcohol
standard_normal_alcohol <- ggplot(data, aes(x = alcohol)) +
  geom_density(aes(y = ..density..), fill = "blue", alpha = 0.5) +
  stat_function(fun = dnorm, args = list(mean = mean(data$alcohol, na.rm = TRUE), sd = sd(data$alcohol, na.rm = TRUE)), color = "red", size = 1) +
  labs(title = "Standard Normal Distribution Plot for Alcohol", x = "Alcohol", y = "Density") +
  theme_minimal() +
  theme_settings
ggsave("standard_normal_alcohol.png", plot = standard_normal_alcohol, width = 10, height = 6)

# Grubbs Test: Acidity
grubbs_test_acidity <- grubbs.test(data$acidity)

# Grubbs Test: Alcohol
grubbs_test_alcohol <- grubbs.test(data$alcohol)

# ANOVA: Acidity
anova_acidity <- aov(acidity ~ as.factor(quality), data = data)
anova_summary_acidity <- summary(anova_acidity)

# ANOVA: Alcohol
anova_alcohol <- aov(alcohol ~ as.factor(quality), data = data)
anova_summary_alcohol <- summary(anova_alcohol)

# Format p-values to 8 decimal places
format_p_value_human <- function(p_value) {
  sprintf("%.8f", p_value)
}

# Format Grubbs test results
grubbs_test_acidity_formatted <- list(
  Statistic = grubbs_test_acidity$statistic,
  p_value = format_p_value_human(grubbs_test_acidity$p.value)
)
grubbs_test_alcohol_formatted <- list(
  Statistic = grubbs_test_alcohol$statistic,
  p_value = format_p_value_human(grubbs_test_alcohol$p.value)
)

# Format ANOVA results
anova_acidity_f_value <- anova_summary_acidity[[1]]["as.factor(quality)", "F value"]
anova_acidity_p_value <- anova_summary_acidity[[1]]["as.factor(quality)", "Pr(>F)"]

anova_alcohol_f_value <- anova_summary_alcohol[[1]]["as.factor(quality)", "F value"]
anova_alcohol_p_value <- anova_summary_alcohol[[1]]["as.factor(quality)", "Pr(>F)"]

anova_results_formatted <- data.frame(
  Variable = c("Acidity", "Alcohol"),
  F_value = c(format_p_value_human(anova_acidity_f_value), format_p_value_human(anova_alcohol_f_value)),
  p_value = c(format_p_value_human(anova_acidity_p_value), format_p_value_human(anova_alcohol_p_value))
)

# Save results and analysis outputs to an Excel file
write_xlsx(list(
  "Grubbs Test Results" = data.frame(
    Test = c("Acidity", "Alcohol"),
    Statistic = c(grubbs_test_acidity_formatted$Statistic, grubbs_test_alcohol_formatted$Statistic),
    p_value = c(grubbs_test_acidity_formatted$p_value, grubbs_test_alcohol_formatted$p_value)
  ),
  "ANOVA Results" = anova_results_formatted
), path = "wine_quality_analysis_results.xlsx")

cat("Formatted analysis results have been successfully saved to the Excel file.\n")