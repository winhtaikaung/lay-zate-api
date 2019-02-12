from handlers.flight.flight_handler import FlightHandler

flight_routes = [
    # (r'/api/v1/flight/([A-Z]{3})/$', AirportCodeFlightHandler),
    (r'/api/v1/flight/([A-Z]{3})/([0,1]{1})/([1-8]{1})$', FlightHandler)

]
