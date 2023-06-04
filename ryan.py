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