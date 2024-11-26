def check_passw(s1):
    length=len(s1)
    digit=False 
    spchar=False 
    upchar=False
    for ch in s1:
        if ch.isupper()==True:
            upchar = True
        if not ch.isalnum():
            spchar=True
        if ch.isdigit() == True: 
            digit=True; 
    if spchar and upchar and digit and length>=8 : 
        return True
    else: 
        return False


def email_validate(email):
    if '.' in email and '@' in email:
        at=email.rindex('@')
        count_at=email.count("@")
        dot=email.rindex('.')
        flg=True
        if count_at!=1:
            flg=False
        elif dot==0 or dot==len(email)-1:
            flg=False
        elif email[0].isdigit():
            flg=False
        elif at>dot:
            flg=False
        for char in email:
            if not char.isalnum() and char!='.' and char!='_' and char!='@':
                flg=False
                break
        if flg:
            return True
def name(name):
    if len(name) in range(3, 51):
        return True
    
def phoneNumber(phone):
    if len(phone)==10 and phone.isnumeric():
        return True
    
def ageValidate():
    while True:
        trial=int(input("Enter age: "))
        if trial in range(18, 100):
            return trial
        elif trial<18:
            print("Age should be greater than 18")
        elif trial>99:
            print("Age should be less than 100")


def func_run(function, inp, warning):
    while True:
        trial=input(inp)
        if function(trial):
            return trial
        else:
            print(warning)

def menu(options):
    for i in range(len(options)):
        print(f"{i+1}. {options[i]}")

