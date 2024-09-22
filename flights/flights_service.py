import csv
from datetime import datetime

from calculate_success_flights import calculate_success_flights
from flights.flight import Flight

fieldnames = ['flight ID', 'Arrival', 'Departure', 'success']


class FlightService:

    def __init__(self, csv_path):
        self.__csv_path = csv_path
        self.flights = {}
        self.load_csv_file(self.__csv_path)

    def load_csv_file(self, path):
        with open(path, mode='r') as data_file:
            reader = csv.DictReader(data_file, skipinitialspace=True)

            for row in reader:
                cleaned_row = {k.strip(): v.strip() for k, v in row.items()}
                self.flights[cleaned_row["flight ID"]] = cleaned_row

    def append_flight(self, flight: Flight):
        self.append_to_csv_file(flight)
        calculate_success_flights(self.__csv_path)
        self.load_csv_file(self.__csv_path)

    def append_to_csv_file(self, flight: Flight):
        with open(self.__csv_path, mode='a', newline='\n') as file:
            new_line = ",".join([flight.flight_id,
                                 str(datetime.strftime(flight.arrival, '%H:%M')),
                                 str(datetime.strftime(flight.departure, '%H:%M')), "``"])
            file.write(f"\n{new_line}")

    def get_flight(self, flight_id):
        return self.flights[flight_id] if flight_id in self.flights else None

    def does_flight_exists(self, flight_id):
        return True if flight_id in self.flights else False

