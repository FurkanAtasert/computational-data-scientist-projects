install.packages(c("readxl", "dplyr", "ggplot2"))
library(readxl)
library(dplyr)
library(ggplot2)

data <- read_excel("categorical_numeric_dataset.xlsx")

# Define categorical and numeric variables
categorical_variables <- c("cinsiyet", "egitim_derecesi")
numeric_variables <- c("d1", "d2")

# Generate plots and save them as PNG files
plot_counter <- 1
for (i in 1:length(categorical_variables)) {
  for (j in 1:length(numeric_variables)) {
    
    # Line Plot
    line_plot <- ggplot(data, aes_string(x = categorical_variables[i], y = numeric_variables[j], group = 1)) +
      geom_line(stat = "summary", fun = "mean", aes(color = "Mean")) +
      geom_point(stat = "summary", fun = "mean", aes(color = "Mean")) +
      labs(
        title = paste("Line Plot - Comparison of", categorical_variables[i], "and", numeric_variables[j]),
        x = categorical_variables[i],
        y = numeric_variables[j]
      ) +
      theme_bw() +
      theme(
        plot.title = element_text(color = "black"),
        axis.text.x = element_text(color = "black"),
        axis.text.y = element_text(color = "black")
      )
    
    ggsave(filename = paste0("line_plot_", plot_counter, ".png"), plot = line_plot)
    
    # Bar Plot
    bar_plot <- ggplot(data, aes_string(x = categorical_variables[i], y = numeric_variables[j], fill = categorical_variables[i])) +
      geom_bar(stat = "summary", fun = "mean", position = "dodge") +
      labs(
        title = paste("Bar Plot - Comparison of", categorical_variables[i], "and", numeric_variables[j]),
        x = categorical_variables[i],
        y = numeric_variables[j]
      ) +
      theme_bw() +
      theme(
        plot.title = element_text(color = "black"),
        axis.text.x = element_text(color = "black"),
        axis.text.y = element_text(color = "black")
      )
    
    ggsave(filename = paste0("bar_plot_", plot_counter, ".png"), plot = bar_plot)
    
    # Point Plot
    point_plot <- ggplot(data, aes_string(x = categorical_variables[i], y = numeric_variables[j], color = categorical_variables[i])) +
      geom_point(stat = "summary", fun = "mean", size = 3) +
      labs(
        title = paste("Point Plot - Comparison of", categorical_variables[i], "and", numeric_variables[j]),
        x = categorical_variables[i],
        y = numeric_variables[j]
      ) +
      theme_bw() +
      theme(
        plot.title = element_text(color = "black"),
        axis.text.x = element_text(color = "black"),
        axis.text.y = element_text(color = "black")
      )
    
    ggsave(filename = paste0("point_plot_", plot_counter, ".png"), plot = point_plot)
    
    # Box Plot
    box_plot <- ggplot(data, aes_string(x = categorical_variables[i], y = numeric_variables[j], fill = categorical_variables[i])) +
      geom_boxplot() +
      labs(
        title = paste("Box Plot - Comparison of", categorical_variables[i], "and", numeric_variables[j]),
        x = categorical_variables[i],
        y = numeric_variables[j]
      ) +
      theme_bw() +
      theme(
        plot.title = element_text(color = "black"),
        axis.text.x = element_text(color = "black"),
        axis.text.y = element_text(color = "black")
      )
    
    ggsave(filename = paste0("box_plot_", plot_counter, ".png"), plot = box_plot)
    
    plot_counter <- plot_counter + 1
  }
}