from tables import create_tables
import funcs as f
import employee as emp
import admin as adm
import user as user

opts1=['LOGIN', 'REGISTER', 'Exit']
opts2=['User', 'Employee', 'Admin', 'BACK']
opts3=['New User', 'Apply for Employee','BACK']

create_tables()
dem=1
print("*^"*15,' WELCOME TO THE LUNAR LEGACY INN ', "^*"*15)
while dem==1:
    f.menu(opts1)
    log=int(input(">>>"))
    if log==1:
        f.menu(opts2)
        role=int(input("Select Role: "))
        if role==1:
            user.user_view()
        elif role==2:
            emp.employeeView()
        elif role==3:
            adm.adminView()
        elif role==4:
            pass
    elif log==2:
        f.menu(opts3)
        opt=int(input("Select>>>"))
        if opt==1:
            user.SignUp()
        elif opt==2:
            emp.job_application()
        elif opt==3:
            pass
    elif log==3:
        exit(0)
