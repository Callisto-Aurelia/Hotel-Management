from texttable import Texttable
import mysql.connector as sql
import funcs as f
import datetime
room_fields=['ROOM_NO', 'CATEGORY', 'RENT']
room_dtype=['t','i','i']


def User_Login():
    con=sql.connect(host='localhost', user='root', passwd='root', database='hotel_management')
    mycursor=con.cursor()
    email=input("Enter your E-mail: ")
    passwd=input("Enter your password: ")
    query='select * from users where email = %s and passwd = %s'
    val=(email, passwd)
    mycursor.execute(query,val)
    result=mycursor.fetchone()
    con.close()
    if result:
        return email
    else:
        return False


def SignUp():
    con=sql.connect(host='localhost', user='root', passwd='root', database='hotel_management')
    mycursor=con.cursor()
    name=f.func_run(f.name, 'Enter Name: ', 'Please enter name of valid length.')
    email=f.func_run(f.email_validate, 'Enter Email: ', 'Invalid Email, please try again.')
    passwd=f.func_run(f.check_passw, 'Enter your password: ', 'Password too weak, please try again.')
    phone=f.func_run(f.phoneNumber, 'Enter your Phone Number: ', 'Invalid Phone Number, please try again.')
    age=f.ageValidate()

    query='insert into users values(%s,%s,%s,%s,%s)'
    val=(name,email,passwd,phone,age)
    mycursor.execute(query,val)
    query=f"insert into user_bill values('{email}', 0, 0)"
    mycursor.execute(query)
    print("Successfully Registered! Please login with your credentials.")
    con.commit()
    con.close()
    
    
def Book_Room(email):
    con=sql.connect(host='localhost', user='root', passwd='root', database='hotel_management')
    mycursor=con.cursor()
    query='select room_no, category, rent from rooms where alloted_to is NULL'
    mycursor.execute(query)
    result=mycursor.fetchall()
    if result:
        result.insert(0, room_fields)
        t=Texttable()
        t.add_rows(result)
        print(t.draw())
    else:
        return print('No rooms available')
    print()
    a=input('Enter room number to book (0 for back): ')
    if a==0:
        pass
    else:
        mycursor.execute(f"select room_no, category, rent from rooms where alloted_to is NULL and room_no='{a}';")
        result=mycursor.fetchone()
        if result:
            fields=['ROOM_NO', 'CATEGORY', 'RENT']
            print('You have selected: ')
            for i in range(0, len(fields)):
                    print(f"{i+1}. {fields[i]}: {result[i]}")
            d=int(input("Enter number of days(0 to cancel): "))
            if d==0:
                pass
            else:
                bill=d*int(result[2])
                date_in=datetime.datetime.today()
                date_out=date_in+datetime.timedelta(days=d)
                str_dIN=date_in.strftime("%Y-%m-%d")
                str_dOUT=date_out.strftime("%Y-%m-%d")
                mycursor.execute(f"update rooms set alloted_to='{email}', date_in='{str_dIN}', date_out='{str_dOUT}' where room_no={a}")
                mycursor.execute(f"update user_bill set room_rent=room_rent+{bill}, no_of_days={d} where email='{email}'")
                print("CONGRATS! ROOM BOOKED SUCCESSFULLY!")
                con.commit()
                con.close()
        else:
            print("This Room is already registered.")

def check_bill(email):
    con=sql.connect(host='localhost', user='root', passwd='root', database='hotel_management')
    mycursor=con.cursor()
    query=f"select room_rent from user_bill where email='{email}'"
    mycursor.execute(query)
    result=mycursor.fetchone()
    bill=result[0]
    print(f"Dear User, your total bill is ₹{bill}")
    
def user_view():
    email=User_Login()
    if email:
        print("Successfully Logged in as USER.")
        while True:
            print("\n"*2)
            print('-_'*15,"USER OPTIONS",'_-'*15)
            opts=["Book a room", "Check Bill", "LOGOUT"]
            f.menu(opts)
            
            n=int(input(">>>"))
            if n==1:
                Book_Room(email)
            elif n==2:
                check_bill(email)
            elif n==3:
                print("Logged out successfully!")
                break
            # except
            #     print("Invalid Value Entered.")
    else:
        print("Login Failed! Please check your credntials and try again.")