library(tidyverse)
library(ggplot2)
library(ggmap)

wifi_data <- read_csv("wifi_data.csv")

# Summary statistics by location
wifi_data %>%
  group_by(x, y) %>%
  summarize(
    mean_dl = mean(download_speed),
    mean_ul = mean(upload_speed),
    median_lat = median(latency)
  )

# Heatmap of download speeds
ggmap(mapdenywc) +
  geom_tile(data = wifi_data,
            aes(x = x, y = y, fill = download_speed)) +
  scale_fill_gradient(low="yellow", high="red")

# Scatterplot of latency vs loss
ggplot(wifi_data, aes(x = latency, y = loss)) +
  geom_point() +
  geom_smooth(method="lm")

# Boxplots comparing locations
ggplot(wifi_data, aes(x = x, y = download_speed)) +
  geom_boxplot() +
  facet_wrap(~y)

# Create hour column from 0 - 23  
wifi_data <- wifi_data %>%
  mutate(hour = hour(time))

# Aggregate by hour and average speed
hourly_avgs <- wifi_data %>%
  group_by(hour) %>%
  summarize(
    avg_dl = mean(download_speed)
  )

# Plot 
ggplot(hourly_avgs, aes(x = hour, y = avg_dl)) +
  geom_col() +
  labs(title = "Average Download Speed by Time of Day",
       x = "Hour of Day",
       y = "Average Speed (Mb/s)")

# Your existing code to calculate hourly averages
wifi_data <- wifi_data %>%
  mutate(hour = hour(time))

hourly_avgs <- wifi_data %>%
  group_by(hour) %>%
  summarize(
    avg_dl = mean(download_speed),
    .groups = 'drop' # This line is to avoid the "ungrouping" message
  )

# Write the hourly_avgs dataframe to a CSV file
write.csv(hourly_avgs, file = "hourly_average_download_speeds.csv", row.names = FALSE)


# Output summary CSV
summary_data <- wifi_data %>%
  group_by(x, y) %>%
  summarize(
    avg_dl = mean(download_speed),
    avg_ul = mean(upload_speed) 
  )
write_csv(summary_data, "wifi_summary.csv")
