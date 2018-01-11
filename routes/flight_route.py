from handlers.flight.flight_handler import FlightHandler, AirportCodeFlightHandler

flight_routes = [
    (r'/api/v1/flight/([A-Z]{3})/$', AirportCodeFlightHandler),
    (r'/api/v1/flight/([A-Z]{3})/([0,1]{1})/([0-7]{1})/$', FlightHandler)

]
