install.packages(c("readxl", "dplyr", "ggplot2", "naniar", "gridExtra", "scales"))

library(readxl)
library(dplyr)
library(ggplot2)
library(naniar)
library(gridExtra)
library(scales)

file_path <- "hematology_dataset.xlsx"
df <- read_excel(file_path, col_names = TRUE)

# Preview the first few rows of the dataset
print(head(df))
missing_df <- miss_var_summary(df)

# Create a plot for missing observations
p_missing_with_missing <- ggplot(
  data = missing_df %>% filter(variable %in% c("WBC", "RBC", "HB", "HCT")),
  aes(x = variable, y = n_miss, fill = variable)
) +
  geom_bar(stat = "identity", position = "dodge") +
  ggtitle("Histogram of Missing Observation Counts") +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    panel.background = element_rect(fill = "white")
  ) +
  xlab("Data Columns") +
  ylab("Number of Missing Observations") +
  scale_fill_manual(values = c("WBC" = "blue", "RBC" = "red", "HB" = "green", "HCT" = "purple"))

ggsave("missing_values_histogram.png", plot = p_missing_with_missing, width = 8, height = 6, units = "in", dpi = 300)

# Function to identify outliers
identify_outliers <- function(df, column) {
  q1 <- quantile(df[[column]], 0.25, na.rm = TRUE)
  q3 <- quantile(df[[column]], 0.75, na.rm = TRUE)
  iqr <- q3 - q1
  lower_bound <- q1 - 1.5 * iqr
  upper_bound <- q3 + 1.5 * iqr
  df %>%
    mutate(outlier = ifelse(df[[column]] < lower_bound | df[[column]] > upper_bound, TRUE, FALSE))
}

# Detect outliers for the selected columns
df_wbc <- identify_outliers(df, "WBC")
p_outliers_wbc <- ggplot(df_wbc, aes(x = factor(0), y = WBC, color = outlier)) +
  geom_boxplot() +
  geom_jitter(width = 0.1, alpha = 0.5) +
  scale_color_manual(values = c("blue", "red"), labels = c("Normal", "Outlier")) +
  ggtitle("Outlier Plot for the WBC Column") +
  xlab("WBC (White Blood Cells)") +
  ylab("Value")

df_rbc <- identify_outliers(df, "RBC")
p_outliers_rbc <- ggplot(df_rbc, aes(x = factor(0), y = RBC, color = outlier)) +
  geom_boxplot() +
  geom_jitter(width = 0.1, alpha = 0.5) +
  scale_color_manual(values = c("blue", "red"), labels = c("Normal", "Outlier")) +
  ggtitle("Outlier Plot for the RBC Column") +
  xlab("RBC (Red Blood Cells)") +
  ylab("Value")

df_hb <- identify_outliers(df, "HB")
p_outliers_hb <- ggplot(df_hb, aes(x = factor(0), y = HB, color = outlier)) +
  geom_boxplot() +
  geom_jitter(width = 0.1, alpha = 0.5) +
  scale_color_manual(values = c("blue", "red"), labels = c("Normal", "Outlier")) +
  ggtitle("Outlier Plot for the HB Column") +
  xlab("HB (Hemoglobin)") +
  ylab("Value")

df_hct <- identify_outliers(df, "HCT")
p_outliers_hct <- ggplot(df_hct, aes(x = factor(0), y = HCT, color = outlier)) +
  geom_boxplot() +
  geom_jitter(width = 0.1, alpha = 0.5) +
  scale_color_manual(values = c("blue", "red"), labels = c("Normal", "Outlier")) +
  ggtitle("Outlier Plot for the HCT Column") +
  xlab("HCT (Hematocrit)") +
  ylab("Value")

# Save the plots
ggsave("wbc_outliers.png", plot = p_outliers_wbc, width = 8, height = 6, units = "in", dpi = 300)
ggsave("rbc_outliers.png", plot = p_outliers_rbc, width = 8, height = 6, units = "in", dpi = 300)
ggsave("hb_outliers.png", plot = p_outliers_hb, width = 8, height = 6, units = "in", dpi = 300)
ggsave("hct_outliers.png", plot = p_outliers_hct, width = 8, height = 6, units = "in", dpi = 300)