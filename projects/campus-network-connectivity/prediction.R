library(tidyverse)
library(ggplot2)
library(ggmap)

# K-means clustering
set.seed(123)
km <- kmeans(wifi_data %>% select(download_speed, upload_speed, latency), centers = 5)

# Add cluster assignment
wifi_data <- wifi_data %>%
  mutate(cluster = km$cluster)

# Compare cluster centers
aggregate(cbind(download_speed, upload_speed, latency) ~ cluster, 
          data = wifi_data, FUN = mean)

# Random forest model  
library(randomForest)
rf_model <- randomForest(download_speed ~ ., data = wifi_data)
wifi_data$rf_pred <- predict(rf_model, wifi_data) 

# Map residuals
ggmap(mapdenywc) +
  geom_point(data = wifi_data, 
             aes(x = x, y = y, col = download_speed - rf_pred))

# Principal component analysis  
pca_result <- prcomp(wifi_data %>% select(download_speed, upload_speed, latency, loss))

ggplot(data.frame(pca_result$x),
       aes(x = PC1, y = PC2)) +
  geom_point()