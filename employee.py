import mysql.connector as sql
from texttable import Texttable
from datetime import datetime
from mysql.connector import Error
import funcs as f
        
# Prepare the header and data for the table
roomFields=["ROOM_NO", "CATEGORY", "ALLOTED_TO","RENT", "DATE_IN", "DATE_OUT"]
roomDtype=['t', 't', 't', 'i', 't', 't'] # Set column data types
user_Fields=["NAME", "EMAIL", 'PHONE_NO', 'AGE', 'ROOM_NO', 'RENT', 'DATE_IN', 'DATE_OUT']
user_Dtypes=['t', 't', 't', 'i', 'i', 'i', 't', 't']

def view(subj, fields, dtype):
    con = sql.connect(host="localhost",  
                    user="root",       
                    passwd="root",     
                    database="hotel_management")
    try:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {subj}")
        result = cur.fetchall()
        
        if result:
            result.insert(0, fields)
            t = Texttable(0)
            t.set_cols_dtype(dtype)
            t.add_rows(result) # Add the result row
            print(t.draw()) # Print the formatted table
            return True
        else:
            print("NOTHING TO SEE HERE....")
            return False
    finally:
        con.close()  # Ensures the connection is closed 

# Function to insert job application into the database
def job_application():
    con = sql.connect(host="localhost",  
                    user="root",       
                    passwd="root",     
                    database="hotel_management")
    cur = con.cursor()

    # Collecting job application details from user
    print("Please fill out your job application details:")

    name=f.func_run(f.name, 'Enter Name: ', 'Please enter name of valid length.')
    email=f.func_run(f.email_validate, 'Enter Email: ', 'Invalid Email, please try again.')
    passwd=f.func_run(f.check_passw, 'Enter your password: ', 'Password too weak, please try again.')
    phone_no=f.func_run(f.phoneNumber, 'Enter your Phone Number: ', 'Invalid Phone Number, please try again.')
    age=f.ageValidate()
    designation = input("Designation Applied For: ")
    DOJ = datetime.now().date()  # Gives the date as YYYY-MM-DD

    # Insert data into the job_applications table
    query = 'insert into applications(name, email, passwd, phone_no, age, designation, DOJ) values(%s, %s, %s, %s, %s, %s, %s)'
    
    values = (name, email, passwd, phone_no, age, designation, DOJ)

    try:
        cur.execute(query, values)
        con.commit()
        print("Job application submitted successfully!")
    except Error as e:
        print("Error inserting data into MySQL table:", e)
        con.rollback()

def employeeLogin():
    con=sql.connect(host='localhost', user='root', passwd='root', database='hotel_management')
    mycursor=con.cursor()
    email=input("Enter E-mail: ")
    passwd=input("Enter password: ")
    query='select * from employees where email = %s and passwd = %s'
    val=(email, passwd)
    mycursor.execute(query,val)
    result=mycursor.fetchone()
    con.close()    
    if result:
        return True
    else:
        return False

# Main function to drive the application
def employeeView():
    login=employeeLogin()
    if login:
        print('Logged in as Employee')
        # Menu to select actions
        while True:
            print("\n"*2)
            print("-"*15,"EMPLOYEE ACTIONS","-"*15)
            print("1. ROOMS")
            print("2. VIEW USERS")
            print("3. Logout")
            try:
                choice = input("Enter your choice: ")

                if choice == '1':
                    print("1. View All Rooms")
                    print("2. View Occupied Rooms")
                    print("3. View Vacant Rooms")
                    print("4. BACK")
                    choice2 = int(input("Enter your choice: "))
                    if choice2 == 1:
                        view('rooms', roomFields, roomDtype)
                    elif choice2 == 2:
                        view('occupied', roomFields, roomDtype)
                    elif choice2 == 3:
                        view('vacant', roomFields, roomDtype)
                    elif choice2 == 4:
                        pass
                elif choice == '2':
                    view('empview', user_Fields, user_Dtypes)
                elif choice == '3':
                    print("Logged out Successfully.")
                    break
                else:
                    print("Invalid choice!!")
            except:
                print("Invalid Value entered.")
    else:
        print("Login Failed. Check your details and try again.")