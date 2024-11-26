import csv
import mysql.connector as sql

def automate(filename, db, query):
    obj=open(filename, 'r')
    reader=csv.reader(obj)
    con=sql.connect(host='localhost', user='root', passwd='root', database=db)
    cursor = con.cursor()
    for r in reader:
        cursor.execute(query, r)
    con.commit()
    con.close()

que='insert into rooms (room_no, category, rent) values(%s, %s, %s)'
automate('hii.csv', 'hotel_management', que)
