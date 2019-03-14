# LayZate Api

Layzate api to provide the real time flight list and flight details information for each airport
The API is [REST API](http://en.wikipedia.org/wiki/Representational_State_Transfer "RESTful") and currently, return format for all endpoints is [JSON](http://json.org/ "JSON").

- [Endpoints](#Endpoints)
- [Running App](#runningapp)
- [FAQ](#faq)
- [Credits](#credits)
- [Contributing](#contributing)
- [License](#license)

# Endpoints

Base URL : http://layzate.herokuapp.com

### Get list of flights from Airport on period of time\*\*

`[GET] /api/v1/{:IATACODE}/{:DEP_ARV}/{POT}?limit={limit}&page={page}`

Eg http://layzate.herokuapp.com/api/v1/MDL/0/5?limit=100&page=1
| Name |param type| DataType |Format|
|--|--|--|--|
| `IATACODE` |path parameter| `CHAR(3)` |`RGN`|
| `DEP_ARV`(Departure or Arrival) |path parameter| `INTEGER(1)` |`0(or)1`|
| `POT` (Period Of Time of the day)|path parameter| `INTEGER(1)` |`range from 1 to 8`|
| `limit`|query parameter| `INTEGER(3)` |`less than equal 100`|
| `page`|query parameter|||

### Get list of flights from Airport on period of time\*\*

`[GET] /api/v1/track/{FLIGHT_CODE}/{FLIGHT_NUMBER}`

Eg. http://layzate.herokuapp.com/api/v1/track/WE/310
| Name |param type| DataType |Format|
|--|--|--|--|
| `FLIGHT_CODE` |path parameter| `CHAR(2)` |`RGN`|
| `FLIGHT_NUMBER` |path parameter| `INTEGER(4)` |``|

## RunningApp

### Prequesties

- mysql
- python 3.7

### Create .env file on root level and configure as following

```env
DB_URL_FORMAT=mysql+pymysql://{}:{}@{}:{}/{}
DB_PASSWORD=123456
git st=localhost
PORT=3000
DB_HOST=your host
DB_PORT=32768
DB_USER_NAME=win
DB_NAME=db_layzate
FLIGHT_BASE_URL=https://www.flightstats.com/go/weblet?guid=34b64945a69b9cac:a51bccf:12d54dfa33f:-5bfe&weblet=status&action=AirportFlightStatus&airportCode={}
TRACK_URL=https://www.flightstats.com/v2/api-next/flight-tracker/{0}/{1}/{2}/{3}/{4}
```

Install all the requirements

```
pip install -r requirements.txt
```

Run the app

```
python3 server.py
```

and open your app at
http://localhost:3000

## FAQ

### Where can I get Airport codes(IATA codes) ?

Here is the list of IATA codes from [datahub](https://github.com/datasets/airport-codes/blob/master/data/airport-codes.csv).

### What do I need to know before I start using the API?

Got any language on your skills? No worries. Here are the docs you might need to get started:

- HTTPS protocol
- [REST software pattern](http://en.wikipedia.org/wiki/Representational_State_Transfer)
- Data serialization with [JSON](http://json.org/) (or see a [quick tutorial](http://www.webmonkey.com/2010/02/get_started_with_json/))

### What return formats do you support?

Layzate API currently returns data in [JSON](http://json.org/ "JSON") format.

### What kind of authentication is required?

N.A

### [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) enabled ?

Yes

## CREDITS

All the flight data and tracking information were extracted by flightstats.com

## Contributing

1. Fork it ( https://github.com/winhtaikaung/lay-zate-api )

2) Create your feature branch (`git checkout -b my-new-feature`)

3. Commit your changes (`git commit -am 'Add some feature'`)

4) Push to the branch (`git push origin my-new-feature`)

5. Create a new Pull Request

## LICENSE

MIT
