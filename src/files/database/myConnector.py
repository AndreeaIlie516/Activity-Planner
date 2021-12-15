import mysql.connector

my_database = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    port='3306',
    database='activity_planner_database'
)

my_cursor = my_database.cursor()

my_cursor.execute('SELECT * FROM persons')

persons = my_cursor.fetchall()

for person in persons:
    print(person)
