import mysql.connector as sql

tables={"USERS":"create table USERS(name varchar(50), email varchar(50) primary key, passwd varchar(50), phone_no varchar(10), age int);",
"EMPLOYEES":"create table EMPLOYEES(name varchar(50), email varchar(50) primary key, passwd varchar(50), phone_no varchar(10), age int, designation varchar(20), DOJ date, salary int);",
"ADMINS":"create table ADMINS(name varchar(50), email varchar(50), passwd varchar(50), phone_no varchar(10));",
"ROOMS":"create table ROOMS(room_no int, category varchar(20), alloted_to varchar(50), rent int, date_in date, date_out date);",
"USER_BILL":"create table USER_BILL(email varchar(50), room_rent int, no_of_days int);",
"useradmview":"create view useradmview as select name, email, phone_no, age from users",
"empadmview":"create view empadmview as select name, email, phone_no, age, designation, doj, salary from employees",
"roomadmview":"create view roomadmview as select * from rooms",
"applications":"create table applications(s_no int PRIMARY KEY AUTO_INCREMENT, name varchar(50), email varchar(50), passwd varchar(50), phone_no varchar(10), age int, designation varchar(20), DOJ date);",
"appadm":"create view appadm as select s_no, name, email, phone_no, age, designation, doj from applications;",
"occupied":"create view occupied as select * from rooms where alloted_to is not null;",
"vacant":"create view vacant as select * from rooms where alloted_to is null;",
"empview":"create view empview as select users.name, users.email, users.phone_no, users.age, rooms.room_no, rooms.rent, rooms.date_in, rooms.date_out from users join rooms on users.email=rooms.alloted_to;"}
def create_tables():
    mydb=sql.connect(host="localhost", user="root",password="root",database="hotel_management")
    mycursor=mydb.cursor()
    mycursor.execute("show tables")
    list_of_tables=[]
    rs=mycursor.fetchall()
    for i in rs:
        list_of_tables.append(i[0])
    for table in tables:
        if table.casefold() not in list_of_tables:
            mycursor.execute(tables[table])
            if table=="ADMINS":
                mycursor.execute("insert into admins values('Dushyant', 'dushyant@gmail.com', 'justforget', '1112223334')")
    mydb.commit()
    mydb.close()
