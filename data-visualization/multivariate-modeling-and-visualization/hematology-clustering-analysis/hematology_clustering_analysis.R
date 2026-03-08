# Install required packages (if not already installed)
install.packages("readxl")
install.packages("dplyr")
install.packages("ggplot2")
install.packages("ggfortify")
install.packages("factoextra")
install.packages("plotly")
install.packages("cluster")
install.packages("psych")

# Load libraries
library(readxl)
library(dplyr)
library(ggplot2)
library(ggfortify)
library(factoextra)
library(plotly)
library(cluster)
library(psych)

# Load the dataset
data <- read_excel("hematology_clinical_dataset.xlsx")

# Select only numeric variables for clustering analysis
clustering_data <- data[, c("WBC", "RBC", "HB", "HCT", "MCV", "MCH", "MCHC", "RDW", "PLT", "MPV", "Lenf", "Monosit", "Nötrofil", "Eozinofil", "Bazofil")]

# K-means clustering analysis
number_of_clusters <- 3
kmeans_model <- kmeans(clustering_data, centers = number_of_clusters, nstart = 20)

# Display cluster centers and assigned cluster labels
print(kmeans_model$centers)
print(kmeans_model$cluster[1:50])

# Add cluster labels to the data
clustering_data <- cbind(clustering_data, "Cluster" = kmeans_model$cluster)

# Add age, diagnosis, and device group variables
# Note: These values are randomly generated for demonstration purposes
set.seed(42)
clustering_data$Age <- sample(1:12, nrow(clustering_data), replace = TRUE)
clustering_data$Diagnosis <- sample(1:2, nrow(clustering_data), replace = TRUE)
clustering_data$DeviceGroup <- sample(1:5, nrow(clustering_data), replace = TRUE)

# Label age and diagnosis variables
age_labels <- c("18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-120")
diagnosis_labels <- c("Healthy", "Patient")

clustering_data$Age <- factor(clustering_data$Age, labels = age_labels)
clustering_data$Diagnosis <- factor(clustering_data$Diagnosis, labels = diagnosis_labels)

# Calculate silhouette score
silhouette_score <- silhouette(kmeans_model$cluster, dist(clustering_data[, c("WBC", "RBC", "HB", "HCT", "MCV", "MCH", "MCHC", "RDW", "PLT", "MPV", "Lenf", "Monosit", "Nötrofil", "Eozinofil", "Bazofil")]))

# Print the score to the terminal
cat("Silhouette Score:", mean(silhouette_score[, "sil_width"]), "\n")

# Calculate descriptive statistics
descriptive_stats <- describe(clustering_data)

# Print descriptive statistics to the terminal
print(descriptive_stats)

# Create a 3D plot using plotly
fig <- plot_ly(
  x = clustering_data$Age,
  y = clustering_data$Diagnosis,
  z = clustering_data$DeviceGroup,
  color = as.factor(clustering_data$Cluster),
  type = "scatter3d",
  mode = "markers",
  marker = list(size = 5)
)

fig <- fig %>% layout(
  scene = list(
    xaxis = list(title = "Age"),
    yaxis = list(title = "Diagnosis"),
    zaxis = list(title = "Device Group")
  ),
  title = "3D Clustering Plot"
)

print(fig)

# Create a 2D clustering plot
gg <- ggplot(clustering_data, aes(x = WBC, y = RBC, color = as.factor(Cluster))) +
  geom_point(size = 3) +
  labs(title = "Clustering Analysis", x = "WBC", y = "RBC", color = "Cluster") +
  theme_classic()

# Save the plot as PNG
ggsave(filename = "clustering_plot.png", plot = gg, width = 8, height = 6, dpi = 300)