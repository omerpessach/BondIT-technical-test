import csv
from datetime import datetime, timedelta


csv_path = ""
daily_success_count = 20
flights = []


def is_valid_flight_duration(arrival, departure):
    arrival_time = datetime.strptime(arrival, '%H:%M')
    departure_time = datetime.strptime(departure, '%H:%M')

    if departure_time < arrival_time:
        departure_time += timedelta(days=1)

    time_diff = departure_time - arrival_time

    return time_diff.total_seconds() / 60 >= 180


def calculate_success_flights(path):
    global csv_path
    csv_path = path
    load_csv_file()
    check_flights_success()
    handle_fixed_flights_data()


def load_csv_file():
    with open(csv_path, mode='r') as data_file:
        reader = csv.DictReader(data_file, skipinitialspace=True)
        flight_ids = set()

        for row in reader:
            cleaned_row = ""
            for k, v in row.items():
                k = k.strip if k is str else k
            cleaned_row = {k.strip(): v.strip() for k, v in row.items()}
            if cleaned_row["flight ID"] not in flight_ids:
                flight_ids.add(cleaned_row["flight ID"])
                flights.append(cleaned_row)

    flights.sort(key=lambda x: x['Arrival'])


def check_flights_success():
    temp_daily_success_count = daily_success_count
    for flight in flights:
        if temp_daily_success_count > 0 and is_valid_flight_duration(flight['Arrival'], flight['Departure']):
            flight['success'] = 'success'
            temp_daily_success_count -= 1
        else:
            flight['success'] = 'fail'


def handle_fixed_flights_data():
    fieldnames = ['flight ID', 'Arrival', 'Departure', 'success']
    write_dict_to_csv_file(csv_path, fieldnames, flights)


def write_dict_to_csv_file(path, fieldnames, dict_data):
    if len(dict_data) > 0:
        with open(path, mode='w', newline='\n') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for row in dict_data:
                writer.writerow(row)
