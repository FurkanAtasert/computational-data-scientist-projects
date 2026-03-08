necessary_packages <- c("readxl", "dplyr", "ggplot2", "GGally", "corrplot", "nnet", "MASS", "caret")
for (package in necessary_packages) {
  if (!requireNamespace(package, quietly = TRUE)) {
    install.packages(package)
  }
}

library(readxl)
library(dplyr)
library(ggplot2)
library(GGally)
library(corrplot)
library(nnet)
library(MASS)
library(caret)

data <- read_excel("hematology_clinical_dataset.xlsx")

# Inspect the dataset
print(head(data))

# Check column names
print(colnames(data))

if (!"YAS" %in% colnames(data)) {
  colnames(data)[which(colnames(data) == "yas_in_excel")] <- "YAS"
}

# Categorize age into ranges
data$AgeCategory <- cut(
  as.numeric(data$YAS),
  breaks = c(18, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, 74, 120),
  labels = c("18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-120")
)

# Create a file to store analysis results and interpretations
sink("clinical_analysis_results.txt")

# Correlation Analysis
cat("=============================================\n")
cat("Correlation Analysis Results:\n")
cat("=============================================\n")
cat("Correlation Matrix:\n")
correlation_matrix <- cor(
  data[, c("WBC", "RBC", "HB", "HCT", "MCV", "MCH", "MCHC", "RDW", "PLT", "MPV", "Lenf", "Monosit", "Nötrofil", "Eozinofil", "Bazofil")]
)
print(correlation_matrix)
cat("\n")

# Visualize and save the correlation matrix
corrplot(
  correlation_matrix,
  method = "color",
  type = "upper",
  tl.cex = 0.7,
  addCoef.col = "black",
  title = "Correlation Matrix",
  col = colorRampPalette(c("blue", "white", "red"))(200)
)
dev.copy(png, "correlation_matrix.png")
dev.off()

# Multiple Linear Regression Analysis (YAS as the dependent variable)
cat("=============================================\n")
cat("Multiple Linear Regression Analysis Results for YAS:\n")
cat("=============================================\n")
cat("In this model, we examine the effect of independent variables on predicting age.\n")
cat("Beta coefficients show the effect of each independent variable on age.\n")
cat("If the coefficient is positive, an increase in the related independent variable leads to an increase in age. If the coefficient is negative, the increase leads to a decrease in age.\n")
model_linear_age <- lm(
  YAS ~ WBC + RBC + HB + HCT + MCV + MCH + MCHC + RDW + PLT + MPV + Lenf + Monosit + Nötrofil + Eozinofil + Bazofil,
  data = data
)
print(summary(model_linear_age))
cat("\n")

# Convert beta coefficients into a data frame
beta_coefficients_age <- data.frame(Beta = coef(model_linear_age))
beta_coefficients_age$Predictor <- rownames(beta_coefficients_age)
rownames(beta_coefficients_age) <- NULL

# Visualize and save beta coefficients
p1 <- ggplot(beta_coefficients_age[-1, ], aes(x = reorder(Predictor, Beta), y = Beta)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label = round(Beta, 2)), hjust = -0.2) +
  coord_flip() +
  theme_minimal(base_family = "Helvetica", base_size = 14, base_rect_size = 0.5) +
  theme(panel.background = element_rect(fill = "white", colour = "white")) +
  ggtitle("Beta Coefficients of the Linear Regression Model for YAS") +
  xlab("Predictors") +
  ylab("Beta Coefficient") +
  theme(plot.title = element_text(hjust = 0.5))
ggsave("beta_coefficients_age.png", p1, bg = "white")

# Logistic Regression Analysis (TANI as the dependent variable)
cat("=============================================\n")
cat("Logistic Regression Analysis Results for TANI:\n")
cat("=============================================\n")
cat("In this model, we examine the effect of independent variables on predicting diagnosis (healthy or diseased).\n")
cat("Beta coefficients show the effect of each independent variable on diagnosis.\n")
cat("If the coefficient is positive, an increase in the related independent variable leads to an increase in disease risk. If the coefficient is negative, the increase leads to a decrease in disease risk.\n")
data$TANI <- ifelse(data$TANI == "SAĞLIKLI", 0, 1)
model_logistic <- glm(
  TANI ~ WBC + RBC + HB + HCT + MCV + MCH + MCHC + RDW + PLT + MPV + Lenf + Monosit + Nötrofil + Eozinofil + Bazofil,
  data = data,
  family = binomial
)
print(summary(model_logistic))
cat("\n")

# Convert beta coefficients into a data frame
beta_coefficients_diagnosis <- data.frame(Beta = coef(model_logistic))
beta_coefficients_diagnosis$Predictor <- rownames(beta_coefficients_diagnosis)
rownames(beta_coefficients_diagnosis) <- NULL

# Visualize and save beta coefficients
p2 <- ggplot(beta_coefficients_diagnosis[-1, ], aes(x = reorder(Predictor, Beta), y = Beta)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label = round(Beta, 2)), hjust = -0.2) +
  coord_flip() +
  theme_minimal(base_family = "Helvetica", base_size = 14, base_rect_size = 0.5) +
  theme(panel.background = element_rect(fill = "white", colour = "white")) +
  ggtitle("Beta Coefficients of the Logistic Regression Model for TANI") +
  xlab("Predictors") +
  ylab("Beta Coefficient") +
  theme(plot.title = element_text(hjust = 0.5))
ggsave("beta_coefficients_diagnosis.png", p2, bg = "white")

# PCA Analysis and 2D Visualization
cat("=============================================\n")
cat("PCA Analysis Results:\n")
cat("=============================================\n")
cat("In this analysis, we reduce the data into a lower-dimensional space.\n")
cat("PC1 and PC2 are the two principal components that explain the largest variance.\n")
cat("These components are linear combinations of the original variables.\n")
cat("\n")
data_pca <- prcomp(
  data[, c("WBC", "RBC", "HB", "HCT", "MCV", "MCH", "MCHC", "RDW", "PLT", "MPV", "Lenf", "Monosit", "Nötrofil", "Eozinofil", "Bazofil")],
  center = TRUE,
  scale. = TRUE
)
print(summary(data_pca))

# Scatter plot for PC1 and PC2
pc <- predict(
  data_pca,
  data[, c("WBC", "RBC", "HB", "HCT", "MCV", "MCH", "MCHC", "RDW", "PLT", "MPV", "Lenf", "Monosit", "Nötrofil", "Eozinofil", "Bazofil")]
)
pc_df <- data.frame(PC1 = pc[, 1], PC2 = pc[, 2], AgeCategory = data$AgeCategory)
pca_plot <- ggplot(pc_df, aes(x = PC1, y = PC2, color = AgeCategory)) +
  geom_point() +
  ggtitle("PCA Analysis: PC1 and PC2") +
  xlab("PC1") +
  ylab("PC2") +
  theme_minimal(base_family = "Helvetica", base_size = 14, base_rect_size = 0.5) +
  theme(panel.background = element_rect(fill = "white", colour = "white")) +
  theme(plot.title = element_text(hjust = 0.5))
ggsave("pca_plot.png", pca_plot, bg = "white")

sink()