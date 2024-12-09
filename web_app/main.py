from flask import Flask, render_template
import csv
from datetime import datetime
import datetime


app = Flask(__name__)


current_time = datetime.datetime.now()  
# Function to read data from a CSV file
def extract_data_from_csv(csv_filename):
    # Open the CSV file
    with open(csv_filename, mode='r', newline='', encoding='utf-8') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)

        header = next(csv_reader, None)
        
        # Extract the data into a list
        data = []
        for row in csv_reader:
          try:
              data.append(row)
          except:
              pass
    
    return header, data



# Example usage
csv_filename = 'network_speed_30_11_08_12_1500_2024.csv'  # Replace with your CSV file path
csv_filename_with_streets = 'hit-osm-base-network\\hit-osm-base-network.csv'
header, data = extract_data_from_csv(csv_filename)
header1, data1 = extract_data_from_csv(csv_filename_with_streets)


link_ids = []
Link_direcrtions = []
timestampts = []
speed = []
unique_entries = []

for i in data:
  link_ids.append(i[0])
  Link_direcrtions.append(i[1])
  timestampts.append(i[2])
  speed.append(int(i[3]))
  unique_entries.append(int(i[4]))


streets_with_increased_cars = []

combined = list(zip(link_ids, Link_direcrtions, timestampts, speed, unique_entries))

# Sort the combined list based on the first element of each tuple (list1)
combined.sort(key=lambda x: x[3])

# Unpack the sorted lists
sorted_id, sorted_direction, sorted_Timestamp, sorted_speed, sorted_UniqueEntries = zip(*combined)

# Convert the tuples back to lists (if needed)
sorted_id = list(sorted_id)
sorted_direction = list(sorted_direction)
sorted_Timestamp = list(sorted_Timestamp)
sorted_speed = list(sorted_speed)
sorted_UniqueEntries = list(sorted_UniqueEntries)

current_hour = current_time.hour
# print((current_hour))

avg_speed_per_road={}

# for i in data1:
  
#   avg_speed_per_road[f'{i[0]}'] = [0] * len(data1)
c = 0
streets_info = []
while True:
  if c == 10:
    break
  for i in data1:
    if i[0] == sorted_id[c] and c < 10:
        streets_info.append({'name': i[10], 'city': 'thessaloniki', 'length': '5 miles', 'lat': float(i[1]), 'lng': float(i[2])})
        c += 1
        break


# Sample street data (you can modify this for your exercise)

@app.route('/')
def index():
    # Pass the streets data to the template
    return render_template('index.html', streets=streets_info)

if __name__ == '__main__':
    app.run(debug=False)