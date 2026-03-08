install.packages("readxl")
install.packages("ggplot2")

library(readxl)
library(ggplot2)

data <- read_excel("demographic-mosaic-plots.xlsx", sheet = "Data_set")

create_mosaic_plot <- function(data, x_column, y_column, file_name) {
  png(filename = paste0(file_name, "_mosaic.png"))
  mosaicplot(
    table(data[[x_column]], data[[y_column]]),
    main = paste(x_column, "vs", y_column, "Mosaic Plot"),
    xlab = x_column,
    ylab = y_column,
    color = TRUE
  )
  dev.off()
}

create_mosaic_plot(data, "YAS", "MEDENI_DURUM", "age_vs_marital_status")
create_mosaic_plot(data, "YAS", "CINSIYET", "age_vs_gender")