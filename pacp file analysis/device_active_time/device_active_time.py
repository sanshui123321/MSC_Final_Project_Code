import os
import pandas as pd
import matplotlib.pyplot as plt

OUTPUT_DIR = '/Users/sanshui/Documents/Research Project/bose_speaker/device_active_time'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'output.txt')
RESULT_FILE = os.path.join(OUTPUT_DIR, 'device_active_time.txt')


dateparse = lambda x: pd.datetime.strptime(x, '%b %d, %Y %H:%M:%S.%f000 %Z')

# Use the specified date format for time parsing
df = pd.read_csv(OUTPUT_FILE, sep='\t', names=["timestamp", "length"], 
                 parse_dates=["timestamp"], date_parser=dateparse)

# Extract hours as a new column
df['hour'] = df['timestamp'].dt.hour

# Group by hour and calculate total and total digits
grouped = df.groupby('hour').agg(total_count=('hour', 'size'), total_bits=('length', 'sum'))

# Group by hour and calculate total and total digits
total_count = grouped['total_count'].sum()
total_bits = grouped['total_bits'].sum()

# Calculate the percentage and keep four decimal places
grouped['frequency_percent'] = ((grouped['total_count'] / total_count) * 100).round(4)
grouped['bits_percent'] = ((grouped['total_bits'] / total_bits) * 100).round(4)

# Change the index to a string in the format 00:00~01:00
grouped.index = [f"{hour:02d}:00~{hour+1:02d}:00" for hour in grouped.index]

grouped[['frequency_percent', 'bits_percent']].to_csv(RESULT_FILE, sep='\t')

# Use the matplotlib library to plot the results
time_intervals = grouped.index
plt.figure(figsize=(12, 7))
line1, = plt.plot(time_intervals, grouped['frequency_percent'], '-o', label='Communication Frequency (%)')
line2, = plt.plot(time_intervals, grouped['bits_percent'], '-s', label='Data Volume (%)')
plt.xlabel('Hour Interval')
plt.ylabel('Percentage (%)')
plt.xticks(rotation=45)
plt.legend()

# Mark the value of each point and adjust its position
for i, txt in enumerate(grouped['frequency_percent']):
    plt.annotate(f"{txt}%", (i, grouped['frequency_percent'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center')
    
for i, txt in enumerate(grouped['bits_percent']):
    plt.annotate(f"{txt}%", (i, grouped['bits_percent'].iloc[i]), textcoords="offset points", xytext=(0,-15), ha='center')

plt.title('IoT Device Activity by Hour')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'activity_chart.png'))
plt.show()
