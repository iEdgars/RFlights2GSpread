import sqlite3

# Connect to the database (if it doesn't exist, it will be created)
conn = sqlite3.connect('ryan.db')

# Create a cursor object
cursor = conn.cursor()

# Create the table
cursor.execute('''CREATE TABLE destinations 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   originAirportCode CHAR(3), 
                   destinationAirportCode CHAR(3))''')

# Create the airports table
cursor.execute('''CREATE TABLE airports 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   airportCode CHAR(3), 
                   airportName TEXT, 
                   airportSeoName TEXT, 
                   airportCountryCode CHAR(2), 
                   airportCountryName TEXT, 
                   airportCityName TEXT, 
                   airportTimeZone TEXT, 
                   currency CHAR(3), 
                   latitude REAL, 
                   longitude REAL, 
                   dateChecked DATETIME)''')

# Commit the changes
conn.commit()

# Close the connection
conn.close()