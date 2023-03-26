import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('example.db')

# Create a cursor object to execute SQL statements
c = conn.cursor()

# Create a new table called "users"
c.execute('''CREATE TABLE users
             (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

# Commit the changes and close the connection
conn.commit()
conn.close()