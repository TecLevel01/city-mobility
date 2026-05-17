import psycopg2

myConnect = psycopg2.connect(
    database='project',
    user='postgres',
    port='5432',
    host='localhost',
    password='admin'

)


# create cursor

cur = myConnect.cursor()


if (myConnect):
    print('connected successfully to PostgreSQL')
else:
    print('Not connected')
