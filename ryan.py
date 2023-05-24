from datetime import date, timedelta, datetime

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


def readDestinationsOld(origin: str, destinationsJSON, destinationsList: list, airportsList: list):
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
        dlatitude = str(d['arrivalAirport']['coordinates']['latitude'])
        dlongitude = str(d['arrivalAirport']['coordinates']['longitude'])
        dDateChecked = str(date.today())
        destinationsList.append([origin, dArrivalAirportCode, dDateChecked])
        airportsList.append([dArrivalAirportCode, dAirportName, dAirportSeoName, dAirportCountryCode, 
                                 dAirportCountryName, dAirportCityName, dAirportTimeZone, dCurrency, dlatitude, dlongitude, dDateChecked])


def readDestinations(destinationsJSON, destinationsList: list, fireCollection, fireBatch, fireDB):
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
        ref = fireDB.collection('Airpots').document(dArrivalAirportCode)
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
