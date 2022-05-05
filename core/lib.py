from abc import ABC, abstractmethod
from enum import Enum


class TransportMode(Enum):
    TRAIN = 'Train'
    BUS = 'Bus'
    AIRPLANE = 'Airplane'

    @classmethod
    def has_value(cls, value):
        return value in {cls.TRAIN, cls.BUS, cls.AIRPLANE}

    @classmethod
    def to_transport_mode(cls, str_value):
        if str_value == 'Train':
            return cls.TRAIN
        elif str_value == 'Bus':
            return cls.BUS
        elif str_value == 'Airplane':
            return cls.AIRPLANE

    @classmethod
    def metadata(cls, mode, key=None):
        if mode == cls.TRAIN:
            md = {'station': 'railway station', 'vehicle': 'train'}
        elif mode == cls.BUS:
            md = {'station': 'bus stop', 'vehicle': 'bus'}
        elif mode == cls.AIRPLANE:
            md = {'station': 'airport', 'vehicle': 'flight'}
        else:
            raise NotImplementedError(f"No transport mode data found for {mode}")
        return md if key is None else md.get(key)


class Location:
    """
    A location in a city. Smallest unit of geo location in the problem domain.
    """

    def __init__(self, name: str, city: str):
        self.name = name
        self.city = city

    def __repr__(self):
        return f"Location<{self.name}, {self.city}>"

    def __str__(self):
        return f"{self.name}, {self.city}"

    def __eq__(self, other):
        return other is not None and other.name == self.name and other.city == self.city


class TripStation:
    """
    Represents a station/stop for a transport-mode.
    For example, a flight terminal, a bus stop, a train station, etc.
    """

    def __init__(self, location: Location, code: str, transport_mode: TransportMode):
        self.location = location
        self.code = code
        if TransportMode.has_value(transport_mode):
            self.transport_mode = transport_mode
        else:
            raise ValueError(f"'{transport_mode}' station not supported")

    def __eq__(self, other):
        return other is not None and other.code == self.code and other.transport_mode == self.transport_mode

    def __str__(self):
        mode_meta_data = TransportMode.metadata(self.transport_mode)
        station = mode_meta_data['station']
        print(type(self.location))
        return f"{self.location.name} ({self.code}) {station} in {self.location.city}"


class TravelPass(ABC):
    """
    An abstract class forming the base for trip passes for different transport modes.
    For example, airplane boarding pass, bus ticket, train ticket, etc.
    """

    def __init__(self, source_station: TripStation,
                 destination_station: TripStation,
                 vehicle_id: str, seat_number: str):
        if source_station.transport_mode != destination_station.transport_mode:
            raise AssertionError("Source and destination cannot be different of transport modes.")
        if source_station == destination_station:
            raise AssertionError("Source and destination stations cannot be same.")
        self.source_station = source_station
        self.destination_station = destination_station
        self.vehicle_id = vehicle_id
        self.seat_number = seat_number

    @abstractmethod
    def vehicle_type(self):
        raise NotImplementedError("Vehicle type not available for the travel pass")

    def narration(self, transport_mode: TransportMode) -> str:
        vehicle = TransportMode.metadata(transport_mode, "vehicle")
        if self.seat_number is None:
            seat_note = "No seat assigned"
        else:
            seat_note = f"Seat # {self.seat_number}"
        return f'Take {vehicle} {self.vehicle_id} from {self.source_station} to {self.destination_station}. {seat_note}'

    def __eq__(self, other):
        return other is not None and self.source_station == other.source_station and self.destination_station == other.destination_station


class TrainTravelPass(TravelPass):

    def __init__(self, source_station: TripStation, destination_station: TripStation,
                 vehicle_id: str, seat_number: str, platform_number: str):
        self.platform_number = platform_number
        if source_station.transport_mode != TransportMode.TRAIN:
            raise AssertionError("Train travel pass cannot be given for non-train transport")
        super().__init__(source_station, destination_station, vehicle_id, seat_number)

    def vehicle_type(self):
        return TransportMode.metadata(TransportMode.TRAIN, "vehicle")

    def __str__(self) -> str:
        if self.platform_number is None:
            platform_note = "Platform # not available"
        else:
            platform_note = f"Platform # {self.platform_number}"
        return f'{super(TrainTravelPass, self).narration(TransportMode.TRAIN)} {platform_note}'


class BusTravelPass(TravelPass):

    def __init__(self, source_station: TripStation, destination_station: TripStation,
                 vehicle_id: str, seat_number: str):
        if source_station.transport_mode != TransportMode.BUS:
            raise AssertionError("Bus travel pass cannot be given for non-bus transport")
        super().__init__(source_station, destination_station, vehicle_id, seat_number)

    def vehicle_type(self):
        return TransportMode.metadata(TransportMode.BUS, "vehicle")

    def __str__(self) -> str:
        return super(BusTravelPass, self).narration(TransportMode.BUS)


class AirTravelPass(TravelPass):

    def __init__(self, source_station: TripStation, destination_station: TripStation,
                 vehicle_id: str, seat_number: str, gate_number: str, baggage_counter: str):
        if source_station.transport_mode != TransportMode.AIRPLANE:
            raise AssertionError("Air travel pass cannot be given for non-air transport")
        self.gate_number = gate_number
        self.baggage_counter = baggage_counter
        super().__init__(source_station, destination_station, vehicle_id, seat_number)

    def vehicle_type(self):
        return TransportMode.metadata(TransportMode.AIRPLANE, "vehicle")

    def __str__(self) -> str:
        if self.baggage_counter is None:
            baggage_note = "Baggage will be automatically transferred from your last leg"
        else:
            baggage_note = f"Baggage drop at counter {self.baggage_counter}"
        return f'{super(AirTravelPass, self).narration(TransportMode.AIRPLANE)}, gate {self.gate_number}. {baggage_note}'


class Trip:
    """
    Represents a trip in a journey. A journey may involve taking multiple trips.
    A `Trip` instance consists of the source location, the destination location and mode of transport
    """

    def __init__(self, boarding_pass: TravelPass):
        self.source: Location = boarding_pass.source_station.location
        self.destination: Location = boarding_pass.destination_station.location
        self.boarding_pass: TravelPass = boarding_pass

    def __str__(self) -> str:
        # return f"From {self.source} to {self.destination} via {self.boarding_pass.vehicle_type()}"
        # return f"To reach from {self.source.name} to {self.destination.name}, {self.boarding_pass}"
        return str(self.boarding_pass)

    def __eq__(self, other):
        return other.boarding_pass == self.boarding_pass


class Journey:
    """
    A class representing journey that consists of one or more trips.
    Implicitly it constructs a linked list of trips sorted based on the correct itinerary, i.e. a trip can be followed
    by last trips destination as its source.

    Assumptions:
    - All trip-stations are directly connected, there is no blind-spot in the journey. For example, if an intermediate
    destination is Albany, then there must be a trip with source as Albany.
    - Any location may be visited at most once per journey, for example a trip to Buffalo, New York airport
    must not be repeated in the journey.
    """

    class Node:
        def __init__(self, trip: Trip, next_node=None):
            self.trip = trip
            self.next_node = next_node

        def __str__(self):
            return f'{self.trip}\n{self.next_node})'

    def __init__(self, trips):
        self.trips = trips

    def sorted_trips(self):
        """
        Sorts a list of unordered trips by chaining their destination-source stations.
        The sorted trips are preserved in a linked list whose head pointer is set as instance variable after sorting.
        """
        if self.trips:
            source_trips = {}  # trips with the key as their source
            destination_trips = {}  # trips with the key as their destination
            head_node = None
            for trip in self.trips:
                source_station = trip.boarding_pass.source_station.code
                destination_station = trip.boarding_pass.destination_station.code
                new_node = self.Node(trip)
                # print(f"-- {source_station} to {destination_station}")
                if destination_station in source_trips:
                    temp_node = source_trips[destination_station]
                    new_node.next_node = temp_node
                    # print(f"-> {new_node.trip.boarding_pass.source_station.code} will point to {destination_station}")
                    head_node = new_node
                if source_station in destination_trips:
                    temp_node = destination_trips[source_station]
                    temp_node.next_node = new_node
                    # print(f"-> {temp_node.trip.boarding_pass.source_station.code} will point to {source_station}")
                if not head_node:
                    head_node = new_node
                source_trips[source_station] = new_node
                destination_trips[destination_station] = new_node

            head = head_node
            while head is not None:
                yield head.trip
                head = head.next_node
