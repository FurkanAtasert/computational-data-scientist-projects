packages <- c("ggplot2", "readxl", "dplyr", "corrplot", "GGally", "openxlsx", "DescTools")
installed_packages <- rownames(installed.packages())

for (pkg in packages) {
  if (!(pkg %in% installed_packages)) {
    install.packages(pkg, dependencies = TRUE)
  }
}

library(ggplot2)
library(readxl)
library(dplyr)
library(corrplot)
library(GGally)
library(openxlsx)
library(DescTools)

# 1. Load and prepare the dataset
data(iris)

# Inspect the dataset
str(iris)
summary(iris)

# 2. Define variable types and perform normality tests
numerical_cols <- c("Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width")
categorical_cols <- c("Species")

# Normality test: Shapiro-Wilk test
normality_results <- sapply(iris[numerical_cols], function(x) {
  shapiro.test(x)$p.value
})

# Print normality test results
print(normality_results)

# Determine whether variables follow a normal distribution
normality <- ifelse(normality_results > 0.05, "Normal", "Not Normal")
names(normality) <- names(normality_results)
print(normality)

# 3a. Numerical-Numerical Correlations: Pearson or Spearman
cor_matrix <- matrix(NA, nrow = length(numerical_cols), ncol = length(numerical_cols))
rownames(cor_matrix) <- numerical_cols
colnames(cor_matrix) <- numerical_cols

for (i in 1:length(numerical_cols)) {
  for (j in 1:length(numerical_cols)) {
    if (i == j) {
      cor_matrix[i, j] <- 1
    } else if (i < j) {
      var1 <- numerical_cols[i]
      var2 <- numerical_cols[j]
      
      if (normality[var1] == "Normal" && normality[var2] == "Normal") {
        # Pearson correlation
        cor_value <- cor(iris[[var1]], iris[[var2]], method = "pearson")
      } else {
        # Spearman correlation
        cor_value <- cor(iris[[var1]], iris[[var2]], method = "spearman")
      }
      
      cor_matrix[var1, var2] <- cor_value
      cor_matrix[var2, var1] <- cor_value
    }
  }
}

# Print the correlation matrix
print(cor_matrix)

# 3b. Categorical-Numerical Associations: Eta Squared
eta_matrix <- matrix(NA, nrow = length(categorical_cols), ncol = length(numerical_cols))
rownames(eta_matrix) <- categorical_cols
colnames(eta_matrix) <- numerical_cols

for (cat_var in categorical_cols) {
  for (num_var in numerical_cols) {
    model <- aov(as.formula(paste(num_var, "~", cat_var)), data = iris)
    eta_squared <- EtaSq(model)
    eta_matrix[cat_var, num_var] <- as.numeric(eta_squared[1, 1])
  }
}

# Print the eta squared matrix
print(eta_matrix)

# 4a. Correlation Heatmap
numeric_corr <- cor(iris[numerical_cols], use = "pairwise.complete.obs", method = "pearson")

png(filename = "Correlation_Heatmap.png", width = 800, height = 600, bg = "white")
corrplot(
  numeric_corr,
  method = "color",
  type = "upper",
  addCoef.col = "black",
  tl.col = "black",
  tl.srt = 45,
  diag = FALSE
)
dev.off()

# 4b. Scatterplot Matrix
p <- ggpairs(
  iris,
  columns = numerical_cols,
  upper = list(continuous = wrap("cor", size = 3)),
  lower = list(continuous = "points"),
  diag = list(continuous = "densityDiag")
) +
  theme_bw() +
  theme(
    panel.background = element_rect(fill = "white"),
    plot.background = element_rect(fill = "white")
  )

ggsave(filename = "Scatterplot_Matrix.png", plot = p, width = 12, height = 10, bg = "white")

# 4c. Correlogram
png(filename = "Correlogram.png", width = 800, height = 800, bg = "white")
corrplot(
  numeric_corr,
  method = "circle",
  type = "full",
  addCoef.col = "black",
  tl.col = "black",
  tl.srt = 45,
  diag = FALSE
)
dev.off()

# 4d. Correlation Network Plot
corr_long <- as.data.frame(as.table(numeric_corr))
corr_long <- corr_long[corr_long$Var1 != corr_long$Var2, ]

# Filter relationships for the network plot (for example, |r| > 0.7)
corr_long_filtered <- corr_long %>% filter(abs(Freq) > 0.7)

p_network <- ggplot(corr_long_filtered, aes(x = Var1, y = Var2, size = abs(Freq), color = Freq)) +
  geom_point(alpha = 0.7) +
  geom_text(aes(label = round(Freq, 2)), vjust = 1.5, size = 3) +
  scale_color_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0) +
  theme_bw() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1, color = "black"),
    axis.text.y = element_text(color = "black"),
    plot.background = element_rect(fill = "white"),
    panel.background = element_rect(fill = "white")
  ) +
  ggtitle("Correlation Network Plot") +
  xlab("") +
  ylab("")

ggsave(filename = "Correlation_Network_Plot.png", plot = p_network, width = 8, height = 6, bg = "white")