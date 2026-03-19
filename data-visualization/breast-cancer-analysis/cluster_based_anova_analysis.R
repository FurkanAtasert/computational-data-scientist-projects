required_packages <- c("ggplot2", "dplyr", "readxl")
new_packages <- required_packages[!(required_packages %in% installed.packages()[, "Package"])]
if (length(new_packages)) install.packages(new_packages)

library(ggplot2)
library(dplyr)
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

breast_cancer_scaled <- scale(breast_cancer[, numeric_vars])

# Recreate clusters so this script can run independently
set.seed(123)
k <- 3
kmeans_result <- kmeans(breast_cancer_scaled, centers = k, nstart = 25)
breast_cancer$Cluster <- as.factor(kmeans_result$cluster)

# Create result folder
if (!dir.exists("results")) {
  dir.create("results")
}
if (!dir.exists("results/anova")) {
  dir.create("results/anova", recursive = TRUE)
}

dependent_var <- "radius_mean"
message(paste("Dependent variable:", dependent_var))

# ANOVA
anova_formula <- as.formula(paste(dependent_var, "~ Cluster"))
anova_model <- aov(anova_formula, data = breast_cancer)
anova_summary <- summary(anova_model)

capture.output(anova_summary, file = "results/anova/anova_summary.txt")
print(anova_summary)

# Tukey HSD
tukey_result <- TukeyHSD(anova_model)
capture.output(tukey_result, file = "results/anova/tukey_hsd_result.txt")
print(tukey_result)

# Boxplot by cluster
plot1 <- ggplot(breast_cancer, aes(x = Cluster, y = .data[[dependent_var]], fill = Cluster)) +
  geom_boxplot() +
  labs(
    title = paste("Distribution of", dependent_var, "by Cluster"),
    x = "Cluster",
    y = dependent_var
  ) +
  theme_bw() +
  theme(
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
    axis.title = element_text(size = 14),
    axis.text = element_text(size = 12),
    legend.title = element_text(size = 14),
    legend.text = element_text(size = 12)
  )

ggsave(
  filename = paste0("results/anova/boxplot_", dependent_var, ".png"),
  plot = plot1,
  width = 10,
  height = 8,
  dpi = 300
)

# Mean values by cluster
mean_values <- breast_cancer %>%
  group_by(Cluster) %>%
  summarise(
    Mean_Value = mean(.data[[dependent_var]], na.rm = TRUE),
    .groups = "drop"
  )

write.csv(
  mean_values,
  paste0("results/anova/mean_values_", dependent_var, ".csv"),
  row.names = FALSE
)

plot2 <- ggplot(mean_values, aes(x = Cluster, y = Mean_Value, fill = Cluster)) +
  geom_bar(stat = "identity") +
  labs(
    title = paste("Mean", dependent_var, "by Cluster"),
    x = "Cluster",
    y = paste("Mean", dependent_var)
  ) +
  theme_bw() +
  theme(
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
    axis.title = element_text(size = 14),
    axis.text = element_text(size = 12),
    legend.title = element_text(size = 14),
    legend.text = element_text(size = 12)
  )

ggsave(
  filename = paste0("results/anova/barplot_mean_", dependent_var, ".png"),
  plot = plot2,
  width = 10,
  height = 8,
  dpi = 300
)

message("ANOVA analysis completed. Results were saved in 'results/anova'.")