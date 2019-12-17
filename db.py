import sqlite3

conn = sqlite3.connect('organisations.db')
# The database will be saved in the location where your 'py' file is saved
c = conn.cursor()

# Create table - CLIENTS
c.execute('''CREATE TABLE ORGANISATIONS
             ([org_id] INTEGER PRIMARY KEY, [org_name] text, [date] date)''')

c.execute('''CREATE TABLE USERS
             ([user_id] INTEGER PRIMARY KEY, [user_name] text, [user_email] text, [user_password] text, [date] date)''')

conn.commit()
