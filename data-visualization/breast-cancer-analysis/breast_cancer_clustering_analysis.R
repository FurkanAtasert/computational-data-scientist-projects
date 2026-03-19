required_packages <- c("ggplot2", "dplyr", "cluster", "factoextra", "readxl")
new_packages <- required_packages[!(required_packages %in% installed.packages()[, "Package"])]
if (length(new_packages)) install.packages(new_packages)

library(ggplot2)
library(dplyr)
library(cluster)
library(factoextra)
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

# K-means clustering (k = 3)
set.seed(123)
k <- 3
kmeans_result <- kmeans(breast_cancer_scaled, centers = k, nstart = 25)
breast_cancer$Cluster <- as.factor(kmeans_result$cluster)

# Create result folder
if (!dir.exists("results")) {
  dir.create("results")
}
if (!dir.exists("results/clustering")) {
  dir.create("results/clustering", recursive = TRUE)
}

plot1 <- fviz_cluster(
  kmeans_result,
  data = breast_cancer_scaled,
  geom = "point",
  ellipse.type = "convex",
  ggtheme = theme_bw()
) +
  labs(
    title = "K-Means Clustering Results (k = 3)",
    x = "Feature 1",
    y = "Feature 2"
  ) +
  theme(
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
    axis.title = element_text(size = 14),
    axis.text = element_text(size = 12),
    legend.title = element_text(size = 14),
    legend.text = element_text(size = 12)
  )

ggsave(
  filename = "results/clustering/kmeans_clustering_results.png",
  plot = plot1,
  width = 10,
  height = 8,
  dpi = 300
)

write.csv(
  breast_cancer,
  "results/clustering/breast_cancer_with_clusters.csv",
  row.names = FALSE
)

capture.output(
  print(kmeans_result),
  file = "results/clustering/kmeans_summary.txt"
)

# Cluster vs Diagnosis comparison table
cluster_diagnosis_table <- table(breast_cancer$Cluster, breast_cancer$Diagnosis)
write.csv(
  as.data.frame.matrix(cluster_diagnosis_table),
  "results/clustering/cluster_diagnosis_table.csv"
)

# Cluster vs Diagnosis comparison plot
plot_cluster_diagnosis <- ggplot(breast_cancer, aes(x = Cluster, fill = Diagnosis)) +
  geom_bar(position = "dodge") +
  labs(
    title = "Cluster Results vs Diagnosis",
    x = "Cluster",
    y = "Count",
    fill = "Diagnosis"
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
  filename = "results/clustering/cluster_vs_diagnosis.png",
  plot = plot_cluster_diagnosis,
  width = 10,
  height = 8,
  dpi = 300
)

message("Clustering analysis completed. Results were saved in 'results/clustering'.")