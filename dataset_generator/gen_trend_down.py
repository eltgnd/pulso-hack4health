import csv
import os
import random
import datetime
import numpy as np

# Function to generate a timestamp
def generate_timestamp(start_date, time_delta):
    return start_date + time_delta

# Initial settings
start_date = datetime.datetime(2023, 1, 1)
end_date = datetime.datetime(2024, 5, 16)
time_interval = datetime.timedelta(minutes=18)  # Time interval between records

# Generate timestamps
timestamps = []
current_date = start_date
while current_date <= end_date:
    timestamps.append(current_date)
    current_date += time_interval

# Generate outcomes with a non-linear decreasing trend
# Using an exponential function to simulate the decrease
probability_decrease = np.exp(np.linspace(3, 0, len(timestamps))) / (np.exp(3))

# Ensure outcomes follow the trend
outcomes = [1 if random.random() < p else 0 for p in probability_decrease]

# Combine timestamps and outcomes
data = list(zip(timestamps, outcomes))


file_name = input("Enter the file name (without extension): ") + ".csv"

# Define the file path to save the CSV file in the datasets folder
file_path = os.path.join('..', 'datasets', file_name)

# Write to CSV
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Date', 'Outcome'])
    for timestamp, outcome in data:
        writer.writerow([timestamp.strftime('%Y-%m-%d %H:%M:%S'), outcome])

print(f"CSV file '{file_name}' has been generated in the 'datasets' folder.")