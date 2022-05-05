from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.lib import BusTravelPass, Location, TransportMode, TripStation, AirTravelPass, TrainTravelPass, Trip, Journey


@api_view(['GET', 'POST'])
def sort_trips(request):
    if request.method == 'GET':
        sample_request = {
            "supported transport modes": ["Airplane", "Train", "Bus"],
            "sample requests": {
                "Airplane": {
                    "transport": {
                        "mode": "Airplane",
                        "vehicle_id": "ABC",
                        "seat_number": "B65",
                        "gate_number": "3A",
                        "baggage_counter": "344",
                    },
                    "source": {
                        "location": {
                            "name": "Buffalo",
                            "city": "New York",
                            "station": "BUF",
                        },
                    },
                    "destination": {
                        "location": {
                            "name": "Albany",
                            "city": "New York",
                            "station": "ALB",
                        }
                    },
                },
                "Train": {
                    "transport": {
                        "mode": "Train",
                        "vehicle_id": "T-12",
                        "seat_number": "B65",
                        "platform_number": "7",
                    },
                    "source": {
                        "location": {
                            "name": "Buffalo",
                            "city": "New York",
                            "station": "BUF",
                        },
                    },
                    "destination": {
                        "location": {
                            "name": "Albany",
                            "city": "New York",
                            "station": "ALB",
                        }
                    },
                },
                "Bus": {
                    "transport": {
                        "mode": "Bus",
                        "vehicle_id": "NY-123",
                        "seat_number": "B65",
                    },
                    "source": {
                        "location": {
                            "name": "Buffalo",
                            "city": "New York",
                            "station": "BUF",
                        },
                    },
                    "destination": {
                        "location": {
                            "name": "Albany",
                            "city": "New York",
                            "station": "ALB",
                        }
                    },
                },
            },
        }
        return Response(sample_request)
    else:
        response = []
        trips = []
        for trip in request.data:
            transport = trip.get("transport")

            source = trip.get("source")
            source_location = Location(source['location']['name'], source['location']['city'])
            source_station = TripStation(source_location, source['location']['station'],
                                         TransportMode.to_transport_mode(transport['mode']))

            destination = trip.get("destination")
            destination_location = Location(destination['location']['name'], destination['location']['city'])
            destination_station = TripStation(destination_location, destination['location']['station'],
                                              TransportMode.to_transport_mode(transport['mode']))

            if TransportMode.to_transport_mode(transport['mode']) == TransportMode.AIRPLANE:
                boarding_pass = AirTravelPass(
                    source_station,
                    destination_station,
                    vehicle_id=transport['vehicle_id'],
                    seat_number=transport['seat_number'],
                    gate_number=transport['gate_number'],
                    baggage_counter=transport['baggage_counter'])

            elif TransportMode.to_transport_mode(transport['mode']) == TransportMode.BUS:
                boarding_pass = BusTravelPass(
                    source_station,
                    destination_station,
                    vehicle_id=transport['vehicle_id'],
                    seat_number=transport['seat_number'])

            elif TransportMode.to_transport_mode(transport['mode']) == TransportMode.TRAIN:
                boarding_pass = TrainTravelPass(
                    source_station,
                    destination_station,
                    vehicle_id=transport['vehicle_id'],
                    seat_number=transport['seat_number'],
                    platform_number=transport['platform_number'])
            else:
                response = {"error": "Transport mode not supported"}
                http_status = status.HTTP_400_BAD_REQUEST
                return Response(response, status.HTTP_400_BAD_REQUEST)
            trips.append(Trip(boarding_pass))
        journey = Journey(trips)
        i = 1
        for trip in journey.sorted_trips():
            response.append(f"{i}. {str(trip)}")
            i += 1
        response.append(f"{i}. You have arrived at your final destination.")
        return Response(response)
