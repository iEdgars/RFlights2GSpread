from datetime import date

baseURL = 'https://www.ryanair.com/api'

def getDestinations(airportFrom: str, version: int):
    if version == 1:
        base = f'{baseURL}/locate/v5/routes'
        departureAirportCode = f'departureAirportCode={airportFrom.upper()}'
        fields = 'fields=arrivalAirport.code&fields=arrivalAirport.name&fields=arrivalAirport.seoName&'\
                  'fields=arrivalAirport.timeZone&fields=arrivalAirport.city.code&fields=arrivalAirport.city.name&'\
                  'fields=arrivalAirport.coordinates.latitude&fields=arrivalAirport.coordinates.longitude&'\
                  'fields=arrivalAirport.country.code&fields=arrivalAirport.country.name&fields=arrivalAirport.country.currency&fields=operator'
        fullURL = f'{base}?{departureAirportCode}&{fields}'
    elif version == 2:
        base = f'{baseURL}/views/locate/searchWidget/routes/en/airport/'
        fullURL = f'{base}{airportFrom.upper()}'

    return fullURL

def getFlights(destination: str, origin: str, Outbound: str, Return: str):
    base = f'{baseURL}/booking/v4/en-en/availability'
    fullURL = f'{base}?ADT=1&CHD=0&Destination={destination}&INF=0&Origin={origin}&TEEN=0&IncludeConnectingFlights=false&DateOut={Outbound}&FlexDaysOut=6&DateIn={Return}&FlexDaysIn=6&RoundTrip=true&ToUs=AGREED'
    
    return fullURL

def readDestinations(destinationsJSON, fireBatch, fireDB):
    destinationsList = []
#read destinations from JSON into list
    for d in destinationsJSON:
        dArrivalAirportCode = d['arrivalAirport']['code']
        dAirportName = d['arrivalAirport']['name']
        dAirportSeoName = d['arrivalAirport']['seoName']
        dAirportCountryCode = d['arrivalAirport']['country']['code']
        dAirportCountryName = d['arrivalAirport']['country']['name']
        dAirportCityName = d['arrivalAirport']['city']['name']
        dAirportTimeZone = d['arrivalAirport']['timeZone']
        dCurrency = d['arrivalAirport']['country']['currency']
        dlatitude = d['arrivalAirport']['coordinates']['latitude']
        dlongitude = d['arrivalAirport']['coordinates']['longitude']
        dDateChecked = int(str(date.today()).replace('-',''))

        #List for Destination on Firebase
        destinationsList.append(dArrivalAirportCode)

        #Setting Firebase batch load of Airports
        ref = fireDB.collection('Airports').document(dArrivalAirportCode)
        fireBatch.set(ref, {
            'AirportCode': dArrivalAirportCode,
            'AirportName': dAirportName,
            'AirportSeoName': dAirportSeoName,
            'AirportCountryCode': dAirportCountryCode,
            'AirportCountryName': dAirportCountryName,
            'AirportCityName': dAirportCityName,
            'AirportTimeZone': dAirportTimeZone,
            'Currency': dCurrency,
            'latitude': dlatitude,
            'longitude': dlongitude,
            'CheckDate': dDateChecked
        })

    return destinationsList

#date / time formatting:
def ryanDateTime(dateTime: str, returnFormat: str='date'):
    #dateTime should be in format YYYY-MM-DDTHH:MM:SS.sss ['2023-01-17T15:55:00.000']
    #returnFormat should be: 
        #date ['2023-01-17'], 
        #dateid ['20230117'], 
        #hour ['15'], 
        #minute ['55'], 
        #time ['15:55'], 
        #datetime ['20230117_15:55'], 
        #dateid:int [20230117], 
        #hour:int [15], 
        #minute:int [55]
    simpleDate = dateTime.split('T')[0]
    dateid = simpleDate.replace('-','')
    hour = dateTime.split('T')[1].split(':')[0]
    minute = dateTime.split('T')[1].split(':')[1]
    time = f"{hour}:{minute}"
    datetime = f"{dateid}_{time}"

    if returnFormat == 'date':
        return simpleDate
    if returnFormat == 'dateid':
        return dateid
    if returnFormat == 'dateid:int':
        return int(dateid)
    if returnFormat == 'hour':
        return hour
    if returnFormat == 'hour:int':
        return int(hour)
    if returnFormat == 'minute':
        return minute
    if returnFormat == 'minute:int':
        return int(minute)
    if returnFormat == 'time':
        return time
    if returnFormat == 'datetime':
        return datetime
    
#read and save flight data
def readFlights(flightsJSON, fireBatch, fireDB):
    for f in flightsJSON['trips']:
        for d in f['dates']:
            if d['flights'] != []:
                for flight in d['flights']:
                    liftoffLocal = flight['time'][0]
                    landingLocal = flight['time'][1]
                    liftoffUTC = flight['timeUTC'][0]
                    landingUTC = flight['timeUTC'][1]
                    refFlightDates = fireDB.collection('Flights').document(f"{f['origin']}-{f['destination']}").collection('FlightDates')
                    #FlightDates collection document
                    ref = refFlightDates.document(f"{f['origin']}-{f['destination']}_{ryanDateTime(flight['time'][0], 'datetime')}")
                    fireBatch.set(ref, {
                        'OriginAirport': f['origin'],
                        'DestinationAirport': f['destination'],
                        'Date': ryanDateTime(d['dateOut'], 'dateid:int'),
                        'FlightNumber': flight['flightNumber'].replace(' ',''),
                        'OperatedBy': flight['operatedBy'],
                        'LiftoffLocalTimeFull': liftoffLocal,
                        'LiftoffLocalTimeHour': ryanDateTime(liftoffLocal, 'hour:int'),
                        'LiftoffLocalTimeMinute': ryanDateTime(liftoffLocal, 'minute:int'),
                        'LandingLocalTimeFull': landingLocal,
                        'LandingLocalTimeHour': ryanDateTime(landingLocal, 'hour:int'),
                        'LandingLocalTimeMinute': ryanDateTime(landingLocal, 'minute:int'),
                        'LiftoffUTCTimeFull': liftoffUTC,
                        'LiftoffUTCTimeHour': ryanDateTime(liftoffUTC, 'hour:int'),
                        'LiftoffUTCTimeMinute': ryanDateTime(liftoffUTC, 'minute:int'),
                        'LandingUTCTimeFull': landingUTC,
                        'LandingUTCTimeHour': ryanDateTime(landingUTC, 'hour:int'),
                        'LandingUTCTimeMinute': ryanDateTime(landingUTC, 'minute:int'),
                        'Duration': flight['duration']
                    })
                    #FlightFares
                    ref2 = refFlightDates.document(f"{f['origin']}-{f['destination']}_{ryanDateTime(flight['time'][0], 'datetime')}").collection('FlightFares').document(str(date.today()).replace('-',''))
                    fireBatch.set(ref2, {
                        'CheckDate': int(str(date.today()).replace('-','')),
                        'FaresLeft': flight['faresLeft'],
                        'FlightKey': flight['flightKey'],
                        'FareClass': flight['regularFare']['fareClass'],
                        'FareType': flight['regularFare']['fares'][0]['type'],
                        'Fare': flight['regularFare']['fares'][0]['amount'],
                        'PublishedFare': flight['regularFare']['fares'][0]['publishedFare'],
                        'HasDiscount': flight['regularFare']['fares'][0]['hasDiscount'],
                        'HasPromoDiscount': flight['regularFare']['fares'][0]['hasPromoDiscount'],
                        'DiscountInPercent': flight['regularFare']['fares'][0]['discountInPercent'],
                        'DiscountAmount': flight['regularFare']['fares'][0]['discountAmount'],
                        'HasBogof': flight['regularFare']['fares'][0]['hasBogof'],
                        'FaresInfantsLeft': flight['infantsLeft']
                    })
        fireDoc = fireDB.collection('Flights').document(f"{f['origin']}-{f['destination']}")
        fireDoc.set({
            'LatestCheckDate': int(str(date.today()).replace('-',''))
        })