import numpy as np


class TrafficCounter:

    def __init__(self, vehicles):
        self.vehicles = vehicles

        # Number of vehicles currently waiting
        self.queue = {
            vehicle.name: 0
            for vehicle in vehicles
        }

        # Fractional departure credits
        self.departure_credit = {
            vehicle.name: 0.0
            for vehicle in vehicles
        }

    def generate_arrivals(self):
        """
        Generate vehicles arriving during this 1-second simulation step.
        """

        arrivals = {}

        for vehicle in self.vehicles:

            number = np.random.poisson(
                vehicle.arrival_rate
            )

            arrivals[vehicle.name] = number

            self.queue[vehicle.name] += number

        return arrivals

    def total_vehicles(self):
        return sum(self.queue.values())

    def weighted_count(self):
        """
        Weighted traffic count.

        Example:
        car  = 1
        bike = 0.5
        SUV  = 1.5
        bus  = 3
        """

        total = 0.0

        for vehicle in self.vehicles:

            total += (
                self.queue[vehicle.name]
                * vehicle.weight
            )

        return total

    def density(self, road_length_km=1.0):
        """
        Traffic density = vehicles / road length.

        We keep this simple for the first simulation.
        """

        return self.total_vehicles() / road_length_km

    def weighted_density(self, road_length_km=1.0):

        return self.weighted_count() / road_length_km

    def process_departures(self, signal_green=True):

        if not signal_green:
            return {}

        departures = {}

        for vehicle in self.vehicles:

            name = vehicle.name

            # Add departure capacity for this second
            self.departure_credit[name] += (
                vehicle.departure_rate
            )

            # Number of vehicles that can leave
            possible_departures = int(
                self.departure_credit[name]
            )

            # Cannot remove more vehicles than are waiting
            actual_departures = min(
                possible_departures,
                self.queue[name]
            )

            self.queue[name] -= actual_departures

            self.departure_credit[name] -= actual_departures

            departures[name] = actual_departures

        return departures