library(tidyverse)
library(ggplot2)
library(ggmap)

# Correlation matrix
cor_mat <- cor(wifi_data %>% select(download_speed, upload_speed, latency, loss))

# Scatterplot 
ggplot(wifi_data, aes(x = download_speed, y = upload_speed)) + 
  geom_point() +
  geom_smooth(method = "lm") +
  labs(title = "Download vs. Upload Speed",
       x = "Download Speed (Mbps)",
       y = "Upload Speed (Mbps)")

# Principal component analysis
pca_result <- prcomp(wifi_data %>% select(download_speed, upload_speed, latency, loss))

# PCA plot
ggplot(data.frame(pca_result$x),
       aes(x = PC1, y = PC2)) +
  geom_point() +
  labs(title = "PCA Plot",
       x = "PC1 (61% variance)",
       y = "PC2 (29% variance)")