import unittest

from core.lib import TripStation, AirTravelPass, Location, TransportMode, Trip, Journey, BusTravelPass, \
    TrainTravelPass


class TripTest(unittest.TestCase):

    def setUp(self) -> None:
        self.source_location = Location("Albany", "New York")
        self.destination_location = Location("Syracuse", "New York")

    def test_create_air_trip(self):
        boarding_pass = AirTravelPass(
            TripStation(self.source_location, "ALB", TransportMode.AIRPLANE),
            TripStation(self.destination_location, "SYR", TransportMode.AIRPLANE),
            vehicle_id="AB-001",
            seat_number="45B", gate_number="3A", baggage_counter="344")

        trip = Trip(boarding_pass)
        self.assertEqual(trip.source, boarding_pass.source_station.location,
                         "Air trip and boarding pass sources do not match")
        self.assertEqual(trip.destination, boarding_pass.destination_station.location,
                         "Air trip and boarding pass destinations do not match")

    def test_create_bus_trip(self):
        boarding_pass = BusTravelPass(
            TripStation(self.source_location, "ALB", TransportMode.BUS),
            TripStation(self.destination_location, "SYR", TransportMode.BUS),
            vehicle_id="BUS-001",
            seat_number="12")

        trip = Trip(boarding_pass)
        self.assertEqual(trip.source, boarding_pass.source_station.location,
                         "Bus trip and boarding pass sources do not match")
        self.assertEqual(trip.destination, boarding_pass.destination_station.location,
                         "Bus trip and boarding pass destinations do not match")

    def test_create_train_trip(self):
        boarding_pass = TrainTravelPass(
            TripStation(self.source_location, "ALB", TransportMode.TRAIN),
            TripStation(self.destination_location, "SYR", TransportMode.TRAIN),
            vehicle_id="T-001",
            seat_number="B63", platform_number="7")

        trip = Trip(boarding_pass)
        self.assertEqual(trip.source, boarding_pass.source_station.location,
                         "Train trip and boarding pass sources do not match")
        self.assertEqual(trip.destination, boarding_pass.destination_station.location,
                         "Train trip and boarding pass destinations do not match")

    def test_boarding_same_source_destination(self):
        with self.assertRaises(AssertionError):
            BusTravelPass(
                TripStation(self.source_location, "ALB", TransportMode.BUS),
                TripStation(self.source_location, "ALB", TransportMode.BUS),
                vehicle_id="BUS-001",
                seat_number="A63")

    def test_boarding_different_transport_modes(self):
        with self.assertRaises(AssertionError):
            TrainTravelPass(
                TripStation(self.source_location, "ALB", TransportMode.TRAIN),
                TripStation(self.destination_location, "SYR", TransportMode.AIRPLANE),
                vehicle_id="BUS-001",
                seat_number="B63", platform_number="7")


class JourneyTest(unittest.TestCase):

    def test_empty_journey(self):
        journey = Journey([])
        self.assertEqual(len(list(journey.sorted_trips())), 0, "Empty journey returned non-zero trips")

    def test_single_trip_journey(self):
        trip = Trip(
            AirTravelPass(
                TripStation(Location("Albany", "New York"), "ALB", TransportMode.AIRPLANE),
                TripStation(Location("Syracuse", "New York"), "SYR", TransportMode.AIRPLANE),
                vehicle_id="AB-001",
                seat_number="45B", gate_number="3A", baggage_counter="344"))
        journey = Journey([trip])
        self.assertListEqual(list(journey.sorted_trips()), [trip, ], "Single trip journey output did not match input")

    def test_journey(self):
        boarding_pass1 = AirTravelPass(
            TripStation(Location("Albany", "New York"), "ALB", TransportMode.AIRPLANE),
            TripStation(Location("Syracuse", "New York"), "SYR", TransportMode.AIRPLANE),
            vehicle_id="AB-001",
            seat_number="45B", gate_number="3A", baggage_counter="344")

        boarding_pass2 = BusTravelPass(
            TripStation(Location("Syracuse", "New York"), "SYR", TransportMode.BUS),
            TripStation(Location("Newburgh", "New York"), "SWF", TransportMode.BUS),
            vehicle_id="NY BUS 01",
            seat_number="12")

        boarding_pass3 = TrainTravelPass(
            TripStation(Location("Newburgh", "New York"), "SWF", TransportMode.TRAIN),
            TripStation(Location("Ithaca", "New York"), "ITH", TransportMode.TRAIN),
            vehicle_id="NY TRAIN 01",
            seat_number="B64", platform_number="7")

        trip1 = Trip(boarding_pass1)
        trip2 = Trip(boarding_pass2)
        trip3 = Trip(boarding_pass3)

        journey = Journey([
            trip3,
            trip2,
            trip1,
        ])

        result = list(journey.sorted_trips())
        self.assertEqual(result,
                         [trip1, trip2, trip3], "Trips are not sorted")
