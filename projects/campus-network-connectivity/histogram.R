# Load tidyr and dplyr
library(tidyr)
library(dplyr)

# Reshape data to long format
wifi_long <- wifi_data %>%
  pivot_longer(
    cols = c(download_speed, upload_speed, latency, loss),
    names_to = "metric",
    values_to = "value"
  )

# Histogram of download speeds
ggplot(data = wifi_long %>% filter(metric == "download_speed")) +
  geom_histogram(aes(x = value), bins = 20) +
  labs(title = "Download Speed Distribution",
       x = "Download Speed (Mbps)",
       y = "Frequency")

# Histogram of upload speeds
ggplot(data = wifi_long %>% filter(metric == "upload_speed")) +
  geom_histogram(aes(x = value), bins = 20) +
  labs(title = "Upload Speed Distribution",
       x = "Upload Speed (Mbps)",
       y = "Frequency")

# Histogram of latency
ggplot(data = wifi_long %>% filter(metric == "latency")) +
  geom_histogram(aes(x = value), bins = 20) +
  labs(title = "Latency Distribution",
       x = "Latency (ms)",
       y = "Frequency")

# Histogram of loss  
ggplot(data = wifi_long %>% filter(metric == "loss")) +
  geom_histogram(aes(x = value), bins = 20) +
  labs(title = "Loss Distribution",
       x = "Loss (%)",
       y = "Frequency")