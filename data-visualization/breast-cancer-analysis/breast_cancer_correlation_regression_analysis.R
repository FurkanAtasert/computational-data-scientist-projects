required_packages <- c("ggplot2", "dplyr", "ggcorrplot", "readxl")
new_packages <- required_packages[!(required_packages %in% installed.packages()[, "Package"])]
if (length(new_packages)) install.packages(new_packages)

library(ggplot2)
library(dplyr)
library(ggcorrplot)
library(readxl)

candidate_files <- c("breast_cancer_data.xlsx", "Breast_Cancer.xlsx")
existing_files <- candidate_files[file.exists(candidate_files)]

if (length(existing_files) == 0) {
  stop("Breast cancer Excel file not found. Make sure 'breast_cancer_data.xlsx' or 'Breast_Cancer.xlsx' is in the same folder as this script.")
}

file_path <- existing_files[1]

breast_cancer <- read_excel(file_path, sheet = 1)
breast_cancer$Diagnosis <- as.factor(breast_cancer$Diagnosis)

numeric_vars <- sapply(breast_cancer, is.numeric)
numeric_vars[names(numeric_vars) %in% c("ID", "Cluster")] <- FALSE

# Create result folder
if (!dir.exists("results")) {
  dir.create("results")
}
if (!dir.exists("results/correlation_regression")) {
  dir.create("results/correlation_regression", recursive = TRUE)
}

# Correlation matrix
cor_matrix <- cor(breast_cancer[, numeric_vars], use = "complete.obs")

plot1 <- ggcorrplot(
  cor_matrix,
  method = "circle",
  type = "lower",
  lab = TRUE,
  lab_size = 3,
  colors = c("red", "white", "blue"),
  title = "Breast Cancer Correlation Matrix",
  ggtheme = theme_bw()
) +
  theme(
    plot.title = element_text(hjust = 0.5, size = 20, face = "bold"),
    axis.title = element_text(size = 16),
    axis.text = element_text(size = 14)
  )

ggsave(
  filename = "results/correlation_regression/correlation_matrix.png",
  plot = plot1,
  width = 20,
  height = 15,
  dpi = 300
)

write.csv(
  cor_matrix,
  "results/correlation_regression/correlation_matrix.csv",
  row.names = TRUE
)

# Multiple linear regression
dependent_var <- "radius_mean"
independent_vars <- setdiff(names(breast_cancer)[numeric_vars], dependent_var)

message(paste("Regression model - Dependent variable:", dependent_var))
message("Independent variables:")
print(independent_vars)

reg_formula <- as.formula(
  paste(dependent_var, "~", paste(independent_vars, collapse = " + "))
)

reg_model <- lm(reg_formula, data = breast_cancer)
reg_summary <- summary(reg_model)

capture.output(
  reg_summary,
  file = "results/correlation_regression/regression_summary.txt"
)

print(reg_summary)

coefficients_df <- as.data.frame(reg_summary$coefficients)
coefficients_df$Variable <- rownames(coefficients_df)
rownames(coefficients_df) <- NULL
names(coefficients_df) <- c("Estimate", "Std_Error", "t_value", "p_value", "Variable")

# Beta coefficient plot
plot_coeff <- ggplot(
  coefficients_df[coefficients_df$Variable != "(Intercept)", ],
  aes(x = reorder(Variable, Estimate), y = Estimate, fill = p_value < 0.05)
) +
  geom_bar(stat = "identity") +
  coord_flip() +
  scale_fill_manual(values = c("grey", "steelblue")) +
  labs(
    title = "Multiple Linear Regression Beta Coefficients",
    x = "Variables",
    y = "Beta Coefficient",
    fill = "Significant (p < 0.05)"
  ) +
  theme_bw() +
  theme(
    plot.title = element_text(hjust = 0.5, size = 20, face = "bold"),
    axis.title = element_text(size = 16),
    axis.text = element_text(size = 14),
    legend.title = element_text(size = 16),
    legend.text = element_text(size = 14)
  )

ggsave(
  filename = "results/correlation_regression/beta_coefficients.png",
  plot = plot_coeff,
  width = 20,
  height = 15,
  dpi = 300
)

# Compare correlation coefficients and beta coefficients
comparison_df <- coefficients_df[coefficients_df$Variable != "(Intercept)", ]
comparison_df$Correlation <- cor_matrix[dependent_var, comparison_df$Variable]

plot_compare <- ggplot(comparison_df, aes(x = Correlation, y = Estimate, color = p_value < 0.05)) +
  geom_point(size = 6) +
  geom_smooth(method = "lm", se = FALSE, color = "black") +
  labs(
    title = "Comparison of Beta Coefficients and Correlation Coefficients",
    x = "Correlation Coefficient",
    y = "Beta Coefficient",
    color = "Significant (p < 0.05)"
  ) +
  theme_bw() +
  theme(
    plot.title = element_text(hjust = 0.5, size = 20, face = "bold"),
    axis.title = element_text(size = 16),
    axis.text = element_text(size = 14),
    legend.title = element_text(size = 16),
    legend.text = element_text(size = 14)
  )

ggsave(
  filename = "results/correlation_regression/beta_vs_correlation.png",
  plot = plot_compare,
  width = 25,
  height = 20,
  dpi = 300
)

message("Correlation and multiple linear regression analysis completed. Results were saved in 'results/correlation_regression'.")