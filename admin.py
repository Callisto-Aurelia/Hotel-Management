import mysql.connector as sql
from texttable import Texttable
import funcs as f

userFields=["NAME", "EMAIL","PHONE_NO", "AGE"]
userDtype=['t','t','t','i']

empFields=["NAME", "EMAIL", "PHONE_NO", "AGE", "DESIGNATION","DOJ" , "SALARY"]
empDtype=['t','t','t','i','t','t','i']

roomFields=["ROOM_NO", "CATEGORY", "ALLOTED_TO","RENT", "DATE_IN", "DATE_OUT"]
roomDtype=['t', 't', 't', 'i', 't', 't']
roomadd=["ROOM_NO", "CATEGORY", "RENT"]

billFields=["EMAIL", "ROOM_RENT", "NUMBER OF DAYS"]
billDtype=['t', 'i', 'i']

appFields=["S.NO.", "NAME", "EMAIL", "PHONE_NO", "AGE","DESIGNATION", "DOJ"]
appDtype=['i', 't', 't', 't', 'i','t', 't']
        
def view(subj, fields, dtype):
    con=sql.connect(host='localhost', user='root', passwd='root', database='hotel_management')
    mycursor = con.cursor()
    mycursor.execute(f"SELECT * FROM {subj}")
    result = mycursor.fetchall()
    if result:
        result.insert(0,fields)
        t=Texttable(0)
        t.set_cols_dtype(dtype)
        t.add_rows(result)
        print(t.draw())
        return True
    else:
        print("NOTHING TO SEE HERE...")
        return False
    con.close()

def edit(table,fields,view):
    con=sql.connect(host='localhost', user='root', passwd='root', database='hotel_management')
    mycursor = con.cursor()
    email=input("Enter the E-mail of person to edit: ")
    mycursor.execute(f"SELECT * FROM {view} WHERE EMAIL='{email}'")
    rec=mycursor.fetchone()
    if rec:
        try:
            for i in range(0, len(fields)):
                print(f"{i+1}. {fields[i]}: {rec[i]}")
            n=int(input("Select the field to edit: "))
            edited_value=input(f"Enter new {fields[n-1]}: ")
            mycursor.execute(f"UPDATE {table} SET {fields[n-1]}='{edited_value}' where email='{email}'")
            con.commit()
            print("Record Updated Successfully.")
        except:
            print("Error Occurred!, Please enter valid value.")
    else:
        print("NOT FOUND!")
    con.close()

def delete(table, fields, view):
    con=sql.connect(host='localhost', user='root', passwd='root', database='hotel_management')
    mycursor=con.cursor()
    email=input("Enter the email of person to delete: ")
    mycursor.execute(f"SELECT * FROM {view} WHERE EMAIL='{email}'")
    rec=mycursor.fetchone()
    if rec:
        for i in range(0, len(fields)):
            print(f"{i+1}. {fields[i]}: {rec[i]}")
        n=input("Are you sure you want to delete this record(y/n): ")
        if n.casefold()=='y':
            mycursor.execute(f"delete from {table} where email='{email}'")
            con.commit()
            print("Record Deleted Successfully!")
        elif n.casefold()=='n':
            print("Reverted!")
        else:
            print("Not Valid.")
    else:
        print("NOT FOUND!")
    con.close()

def roomAdd(fields):
    con=sql.connect(host='localhost', user='root', passwd='root', database='hotel_management')
    mycursor=con.cursor()
    vals=[]
    for field in fields:
        val=input(f"Enter {field}: ")
        vals.append(val)
    query="insert into rooms (room_no, category, rent) values (%s, %s, %s)"
    mycursor.execute(query,vals)
    con.commit()
    print("Room Added Successfully.")
    con.close()

def application(fields):
    con=sql.connect(host='localhost', user='root', passwd='root', database='hotel_management')
    mycursor=con.cursor()
    n=view('appadm', appFields, appDtype)
    if n:
        s_no=int(input("Enter the S_no to select: "))
        mycursor.execute(f"select * from appadm where s_no={s_no}")
        app=mycursor.fetchone()
        if app:
            for i in range(0, len(fields)):
                print(f"{i+1}. {fields[i]}: {app[i]}")
            deci=input("Enter 'A' to approve, 'R' to reject: ")
            if deci.casefold()=='a':
                salary=int(input("Enter salary for this Employee: "))
                mycursor.execute(f"select name, email, passwd, phone_no, age, designation, doj from applications")
                vals=list(mycursor.fetchall()[0])
                vals.append(salary)
                query="insert into employees values(%s, %s, %s, %s, %s, %s, %s, %s)"
                mycursor.execute(query, vals)
                mycursor.execute(f'delete from applications where s_no={s_no}')
                print("EMPLOYEE ADDED SUCCESSFULLY!")
                con.commit()
            elif deci.casefold()=='r':
                mycursor.execute(f'delete from applications where s_no={s_no}')
                con.commit()
                print("Application Rejected.")
            else:
                print("Not a valid choice.")
        else:
            print("Application Doesn't exist.")
    con.close()
    
def adminLogin():
    con=sql.connect(host='localhost', user='root', passwd='root', database='hotel_management')
    mycursor=con.cursor()
    email=input("Enter E-mail: ")
    passwd=input("Enter password: ")
    query='select * from admins where email = %s and passwd = %s'
    val=(email, passwd)
    mycursor.execute(query,val)
    result=mycursor.fetchone()
    con.close()    
    if result:
        return True
    else:
        return False

opts=['USERS', 'EMPLOYEES', 'ROOMS', 'BILLS', 'APPLICATIONS', 'LOGOUT']
subs=['View', 'Edit', 'Delete','BACK']
subs_=['View','Add', 'Edit', 'Delete', 'BACK']

def adminView():
    login=adminLogin()
    if login:
        print("Logged in as ADMIN.")
        while True:
            print("\n"*2)
            print('-'*15,"ADMIN CONTROLS",'-'*15)
            f.menu(opts)
            try:
                n=int(input(">>>"))
                if n==1:
                    f.menu(subs)
                    uN=int(input("Select operation for users: "))
                    if uN==1:
                        view('useradmview', userFields, userDtype)
                    elif uN==2:
                        edit('users', userFields, 'useradmview')
                    elif uN==3:
                        delete('users', userFields, 'useradmview')
                    elif uN==4:
                        pass
                elif n==2:
                    f.menu(subs)
                    eN=int(input("Select operation for employees: "))
                    if eN==1:
                        view('empadmview', empFields, empDtype)
                    elif eN==2:
                        edit('employees', empFields, 'empadmview')
                    elif eN==3:
                        delete('employees', empFields, 'empadmview')
                elif n==3:
                    f.menu(subs_)
                    rN=int(input("Select operation for Rooms (0 to back): "))
                    if rN==1:
                        view('roomadmview', roomFields, roomDtype)
                    elif rN==2:
                        roomAdd(roomadd)
                    elif rN==3:
                        edit('rooms', roomFields, 'roomadmview')
                    elif rN==4:
                        delete('rooms', roomFields, 'roomadmview')
                    elif rN==0:
                        pass
                elif n==4:
                    view('user_bill',billFields, billDtype)
                elif n==5:
                    application(appFields)
                elif n==6:
                    print("Logged out Successfully.")
                    break
            except:
                print("Invalid Value Entered.")
    else:
        print('Login Failed! Please check your credentials and try again.')