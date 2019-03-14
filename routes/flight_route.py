from handlers.flight.flight_handler import FlightHandler
from handlers.flight.flight_handler import AirportCodeFlightHandler

flight_routes = [
    (r'/api/v1/track/([A-Z0-9]{1,2})/([A-Z0-9]{1,4})$',
     AirportCodeFlightHandler),
    (r'/api/v1/([A-Z]{3})/([0,1]{1})/([1-8]{1})$', FlightHandler)

]
