library(tidyverse)
library(ggplot2)
library(ggmap)

# Boxplot of download speeds
ggplot(wifi_data, aes(y = download_speed)) +
  geom_boxplot() +
  labs(title = "Download Speed Distribution",
       y = "Download Speed (Mbps)")

# Boxplot of upload speeds
ggplot(wifi_data, aes(y = upload_speed)) + 
  geom_boxplot() +
  labs(title = "Upload Speed Distribution",  
       y = "Upload Speed (Mbps)")

# Boxplot of latency
ggplot(wifi_data, aes(y = latency)) +
  geom_boxplot() + 
  labs(title = "Latency Distribution",
       y = "Latency (ms)")

# Boxplot of loss
ggplot(wifi_data, aes(y = loss)) +
  geom_boxplot() +
  labs(title = "Loss Distribution",
       y = "Loss (%)")

# Faceted boxplots to compare locations  
ggplot(wifi_data, aes(x = x, y = download_speed)) +
  geom_boxplot() +
  facet_wrap(~y) +
  labs(title = "Download Speed by Location",
       x = "X-Coordinate",
       y = "Download Speed (Mbps)")