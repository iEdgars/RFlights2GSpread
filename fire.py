def fireTrip(fireDB, trip: str, isActive: bool, outboundDate: int, returnDate: int=0):
    fireDoc = fireDB.collection('Trips').document(trip)
    if returnDate != 0:
        fireDoc.set({
            'From': trip[:3],
            'To': trip[4:],
            'Active': isActive,
            'OutboundDate': outboundDate,
            'OneWay': False,
            'ReturnDate': returnDate
        })
    else:
        fireDoc.set({
            'From': trip[:3],
            'To': trip[4:],
            'Active': isActive,
            'OutboundDate': outboundDate,
            'OneWay': True
        })
