import sqlite3
import pandas as pd
from pandas import DataFrame

conn = sqlite3.connect('organisations.db')
c = conn.cursor()

read_orgs = pd.read_csv(r'orgs.csv')
# Insert the values from the csv file into the table 'ORGANISATIONS'
read_orgs.to_sql('ORGANISATIONS', conn, if_exists='append', index=False)

read_users = pd.read_csv(r'users.csv')
# Insert the values from the csv file into the table 'USERS'
read_users.to_sql('USERS', conn, if_exists='append', index=False)

c.execute('''
SELECT DISTINCT *
FROM ORGANISATIONS
WHERE date = (SELECT max(date) FROM ORGANISATIONS)
          ''')

df = DataFrame(c.fetchall(), columns=['org_id','org_name','date'])
print(df)

