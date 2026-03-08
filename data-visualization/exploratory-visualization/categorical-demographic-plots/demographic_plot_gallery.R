install.packages("readxl")
install.packages("ggplot2")
install.packages("ggpubr")
install.packages("qqplotr")

library(readxl)
library(ggplot2)
library(ggpubr)
library(qqplotr)

data <- read_excel("demographic_sample_dataset.xlsx")

# Select the dataset columns to be used in the plots
numeric_data <- data[, c("Sex", "Age", "Married")]

# Map numeric values to their categorical labels
numeric_data$Age <- factor(
  numeric_data$Age,
  levels = c(1, 2, 3, 4),
  labels = c("Under 18", "18-29 years", "29-45 years", "45 years and above")
)

numeric_data$Sex <- factor(
  numeric_data$Sex,
  levels = c(1, 2),
  labels = c("Female", "Male")
)

numeric_data$Married <- factor(
  numeric_data$Married,
  levels = c(1, 2),
  labels = c("Single", "Married")
)

# Scatter Plot - Display the third variable using color or size
scatter_plot <- ggplot(numeric_data, aes(x = Age, y = Married, color = Sex, size = Sex)) +
  geom_point() +
  labs(title = "Scatter Plot", x = "Age", y = "Marital Status") +
  theme_light()

# Box Plot - Use the third variable as a grouping variable
box_plot <- ggplot(numeric_data, aes(x = Sex, y = Age, fill = Sex)) +
  geom_boxplot() +
  labs(title = "Box Plot", x = "Sex", y = "Age") +
  theme_light()

# QQ Plot - Display the third variable using different colors
qq_plot <- ggplot(numeric_data, aes(sample = Age, color = Sex)) +
  stat_qq() +
  stat_qq_line() +
  labs(title = "QQ Plot", x = "Theoretical Quantiles", y = "Sample Quantiles") +
  theme_light()

print(scatter_plot)
print(box_plot)
print(qq_plot)

# Save the plots
ggsave("scatter_plot.png", plot = scatter_plot, width = 6, height = 4)
ggsave("box_plot.png", plot = box_plot, width = 6, height = 4)
ggsave("qq_plot.png", plot = qq_plot, width = 6, height = 4)