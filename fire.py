from datetime import date

#creating trip's based on imputs
def fireTrip(fireDB, trip: str, created: int, isActive: bool, matchingConnections: str, isDirect: bool, outboundDate: int, returnDate: int=0):
    if returnDate != 0:
        fireDoc = fireDB.collection('Trips').document(f'{trip}_o{outboundDate}-r{returnDate}')
        fireDoc.set({
            'From': trip[:3],
            'To': trip[4:],
            'Active': isActive,
            'OutboundDate': outboundDate,
            'OneWay': False,
            'ReturnDate': returnDate,
            'TripCreated': created,
            'Connections': matchingConnections,
            'Direct': isDirect
        })
    else:
        fireDoc = fireDB.collection('Trips').document(f'{trip}_o{outboundDate}-r0')
        fireDoc.set({
            'From': trip[:3],
            'To': trip[4:],
            'Active': isActive,
            'OutboundDate': outboundDate,
            'OneWay': True,
            'TripCreated': created,
            'Connections': matchingConnections,
            'Direct': isDirect
        })


#creating/updating destination info
def fireDestinations(fireDB, origin: str, destinations):
    checkDate = int(str(date.today()).replace('-',''))
    fireDoc = fireDB.collection('Destinations').document(origin)
    fireDoc.set({
        'CheckDate': checkDate,
        'Destinations': destinations
    })
    # fireDoc = fireDB.collection('Destinations').document(origin).collection('HistoricalDestinations').document(f'{checkDate}')
    # fireDoc.set({
    #     'CheckDate': checkDate,
    #     'Origin': origin,
    #     'Destinations': destinations,
    #     'Quantity': len(destinations)
    # })

#adding destination matches
def fireConnections(fireDB, trip: str, matchingConnections: str, isDirect: bool):
    checkDate = int(str(date.today()).replace('-',''))
    tripFrom = trip[:3]
    tripTo = trip[4:]
    fireDoc = fireDB.collection('Destinations').document(tripFrom).collection('Connections').document(tripTo)
    fireDoc.set({
        'CheckDate': checkDate,
        'Trip': trip.split('-'),
        'Destinations': matchingConnections,
        'Quantity': len(matchingConnections),
        'Direct': isDirect
    })
    fireDoc = fireDB.collection('Destinations').document(tripTo).collection('Connections').document(tripFrom)
    fireDoc.set({
        'CheckDate': checkDate,
        'Trip': trip.split('-'),
        'Destinations': matchingConnections,
        'Quantity': len(matchingConnections),
        'Direct': isDirect
    })