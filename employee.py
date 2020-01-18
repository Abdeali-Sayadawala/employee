import pymongo
import datetime
import re
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['company']
emp = db['employee']
salarydb = db['salary']
att = db['attendance']
hol = db['holidays']
fun = db['functions']

def validateEmail(email):
    emailregex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if (re.search(emailregex, email)):
        return True
    else:
        return False
def emailExists(email):
    for i in emp.find():
        if i["email"] == email and i["deleted"] == False:
            return False
        else:
            return True

def validateMobile(mobile):
    try:
        if len(mobile) == 10:
            number = int(mobile)
            return True
        else:
            return False
    except Exception:
        return False
    
def validateDate(date):
    datesplit = date.split('/')
    if len(datesplit) != 3:
        return False
    if len(datesplit[0]) == 2 and len(datesplit[1]) == 2 and len(datesplit[2]) == 4:
        if datesplit[1] in [1,3,5,7,8,10,12] and datesplit[0] > 31:
            return False
        elif datesplit[1] in [4,6,9,11] and datesplit[0] > 30:
            return False
        elif datesplit[1] == 2 and datesplit[0] > 28:
            return False
        else:
            return True
    else:
        return False
        

class Employee:
    def add_employee(self, name, address, status, Dateofbirth, email, mobile):
        i = None
        for x in emp.find():
            i = x
            eid = x["eid"]
        if i == None:
            eid = 1
        else:
            data = emp.find().sort("eid",-1).limit(1)
            for i in data:
                eid = i["eid"]
                eid = eid + 1
        dict = {"eid":eid,"name":name, "address":address, "status":status, "dob":Dateofbirth, "email":email, "mobile":mobile, "deleted": False}
        emp.insert_one(dict)
        print("Id of "+str(name)+" is "+str(eid))
        if status == "intern":
            salarydb.insert_one({"eid":eid, "salary": 7000, "date": datetime.date.today().strftime("%d/%m/%Y")})
        elif status == "GOD":
            salarydb.insert_one({"eid":eid, "salary": 700000, "date": datetime.date.today().strftime("%d/%m/%Y")})
        elif status == "experienced":
            salarydb.insert_one({"eid":eid, "salary": 25000, "date": datetime.date.today().strftime("%d/%m/%Y")})
            
    def display_all(self):
        data = None
        for x in emp.find({}, {"_id":0}):
            data = x
        if data == None:
            print("Id not present.")
            return 0
        data = emp.find({}, {"_id":0, "Address":0, "DateofBirth":0, "Mobile":0})
        for i in data:
            if i["Deleted"] == True:
                continue
            print("Employee ID: ", i["eid"])
            print("Name: ", i["name"])
            print("Status: ", i["status"])
            print("E-mail: ", i["email"])
            print("="*40)

    def display_details(self, eid):
        data = None
        for x in emp.find({"eid": int(eid)}, {"_id":0}):
            data = x
        if data == None: 
            print("Id not present.")
            return 0
        data = emp.find({"eid": int(eid)}, {"_id":0})
        for i in data:
            if i["deleted"] == True:
                print("ID deleted.")
                break
            print("Employee ID: ", i["eid"])
            print("Name: ", i["name"])
            print("Address: ", i["address"])
            print("Status: ", i["status"])
            print("DateofBirth: ", i["dob"])
            print("E-mail: ", i["email"])
            print("Mobile", i["mobile"])
            print("="*40)

    def remove_entry(self, eid):
        data = None
        for x in emp.find({"eid": int(eid)}, {"_id":0}):
            data = x
        if data == None:
            print("Id not present.")
            return 0
        for i in emp.find({"eid": int(eid)}, {"_id":0}):
            if i["deleted"] == True:
                print("ID already deleted.")
                return 0
        emp.update_one({"eid": int(eid)},{"$set": {"deleted": True}})
        print(str(eid)+" removed")

    def update_entry(self, eid):
        data = None
        for x in emp.find({"eid": int(eid)}, {"_id":0}):
            data = x
        if data == None:
            print("Id not present.")
            return 0
        for i in emp.find({"eid": int(eid)}, {"_id":0}):
            if i["Deleted"] == True:
                print("ID already deleted.")
                return 0
        self.display_details(eid)
        print("Update your details:")
        name = input("Name: ")
        address = input("Address: ")
        status = input("Status: ")
        valid = 0
        while valid == 0:
            dob = input("Date of Birth(dd/mm/yyyy): ")
            if validateDate(dob):
                valid = 1
            else:
                print("Invalid Date format.!")
        valid = 0
        while valid == 0:
            email = input("E-mail: ")
            if validateEmail(email):
                if emailExists(email):
                    valid = 1
                else:
                    print("Email already exists try another!.")
            else:
                print("Email Invalid. Please Enter Again!.")
        valid = 0
        while valid == 0:
            mobile = input("Number: ")
            if validateMobile(mobile):
                valid = 1
            else:
                print("Ivalid Mobile Number.!")
        emailregex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if (re.search(emailregex, email)) == False:
            print("Invalid Email")
            return 0
        query = {"eid": int(eid)}
        execute = {"$set": {"name":name, "address":address, "status":status, "dob":dob, "email":email, "mobile":mobile}}
        emp.update_one(query, execute)
        if status == "intern":
            salarydb.update_one({"eid":int(eid)}, {"$set" : {"eid":int(eid), "salary": 7000, "date": datetime.date.today().strftime("%d/%m/%Y")}})
        elif status == "GOD":
            salarydb.update_one({"eid":int(eid)}, {"$set" : {"eid":int(eid), "salary": 700000, "date": datetime.date.today().strftime("%d/%m/%Y")}})
        elif status == "experienced":
            salarydb.update_one({"eid":int(eid)}, {"$set" : {"eid":int(eid), "salary": 25000, "date": datetime.date.today().strftime("%d/%m/%Y")}})
        self.display_details(eid)

class Attendance:
    def mark_attendance(self, eid, present):
        for i in att.find({"eid": int(eid)}, {"_id":0}):
            if i["deleted"] == True:
                print("ID deleted.")
                return 0
        att.insert_one({"eid":eid, "present":present, "date":datetime.date.today().strftime("%d/%m/%Y")})
    def show_all_attendance(self):
        for i in emp.find():
            if i["deleted"] == True:
                continue
            print(i["name"])
            for j in att.find({"eid":i["eid"]},{"_id":0}):
                print(str(j["date"])+"----"+str(j["present"]))

class Salary: 
    def get_salary(self, eid, date = int(datetime.date.today().strftime("%d")), month = int(datetime.date.today().strftime("%m")), year = int(datetime.date.today().strftime("%Y"))):
        count = 0
        holidays = []
        for i in emp.find({"eid": int(eid)}, {"_id":0}):
            if i["deleted"] == True:
                print("ID deleted.")
                return 0
        for i in salarydb.find({"eid":eid},{"_id":0, "eid":0, "salary":0}).sort("_id",-1).limit(1):
            dt = int(i['date'][:2])
        for i in hol.find({"Month":int(datetime.date.today().strftime("%m"))}, {"_id":0}):
            if i["Holiday"] != 0:
                holidays.append(int(i["Day"]))
        for i in att.find({"eid":eid},{"_id":0, "eid":0}).limit(dt):
            if int(i['present']) == 1 or int(i["date"][:2]) in holidays:
                count = count + 1
        for i in salarydb.find({"eid":eid},{"_id":0, "eid":0, "date":0}):
            sal = int(i["salary"])
        if int(month) in [4, 6, 9, 11]:
            if count == 30:
                salary = sal
            else:
                salperday = sal/30
                salary = salperday * count
        elif int(month) == 2:
            if count == 28:
                salary = sal
            else:
                salperday = sal/28
                salary = salperday * count
        else:
            if count == 31:
                salary = sal
            else:
                salperday = sal/31
                salary = salperday * count
        print(int(salary))
        
class Functions:
    def addFunction(self, date, function, budget):
        fun.insert_one({"date": date, "function": function, "budget": budget, "profit":0, "loss":0})
    def showFunctions(self):
        for i in  fun.find({},{"_id":0}):
            print("Date: "+str(i['date']))
            print("Function: "+str(i['function']))
            print("Budget: "+str(i['budget']))
    def showPL(self, date):
        for i in fun.find({"date":date},{"_id":0}):
            print("Date: "+str(i['date']))
            print("Function: "+str(i['function']))
            print("Budget: "+str(i['budget']))
            print("Profit: "+str(i['profit']))
            print("Loss: "+str(i["loss"]))
    def spent(self, date, cost):
        for i in fun.find({"date":date},{"_id":0}):
            pl = int(i['budget']) - cost
            if pl > 0:
                fun.update_one({'date': date}, {"$set":{"profit": pl}})
            else:
                fun.update_one({'date': date}, {"$set": {"loss": pl}})
            
        
while True:
    print("1. Employee Management.")
    print("2. Salary Management.")
    print("3. Attendance Management.")
    print("4. Function Management.")
    print("5. Exit.")
    a1 = int(input("Enter your choice: "))
    if a1 == 1:
        e = Employee()
        print("1. Add employee")
        print("2. Display")
        print("3. Display all")
        print("4. Remove")
        print("5. Update")
        print("6. Back")
        a2 = int(input("Enter your choice: "))
        if a2 == 1:
            name = input("Enter Name: ")
            address = input("Enter Address ")
            valid = 0
            while valid == 0:
                dob = input("Date of Birth(dd/mm/yyyy): ")
                if validateDate(dob):
                    valid = 1
                else:
                    print("Invalid Date format.!")
            status = input("Enter Status (intern/experienced/GOD): ")
            valid = 0
            while valid == 0:
                mobile = input("Enter mobile number: ")
                if validateMobile(mobile):
                    valid = 1
                else:
                    print("Ivalid Mobile Number.!")
            valid = 0
            while valid == 0:
                email = input("Enter your mail: ")
                if validateEmail(email):
                    if emailExists(email):
                        valid = 1
                    else:
                        print("Email already exists try another!.")
                else:
                    print("Email Invalid. Please Enter Again!.")
            e.add_employee(name, address, status, dob, email, mobile)
        if a2 == 2:
            eid = input("Enter Id number of the employee: ")
            e.display_details(eid)
        if a2 == 3:
        	e.display_all()
        if a2 == 4:
            eid = input("Enter ID number of employee to remove: ")
            e.remove_entry(eid)
        if a2 == 5:
            eid = input("Enter ID number of employee to update: ")
            e.update_entry(eid)
        if a2 == 6:
            continue
    elif a1 == 2:
        s = Salary()
        print("1. Get the current salary of employee.")
        print("2. Back.")
        a2 = int(input("Enter your choice: "))
        if a2 == 1:
            eid = int(input("Enter ID of employee to get the salary: "))
            s.get_salary(eid)
        elif a2 == 2:
            continue
    elif a1 == 3:
        a = Attendance()
        print("1. Mark Attendance")
        print("2. Show Attendance")
        print("3. Back")
        a2 = int(input("Enter your choice: "))
        if a2 == 1:
            eid = int(input("Enter ID of employee: "))
            present = int(input("Enter status (1->Present/0->Absent): "))
            a.mark_attendance(eid, present)
        elif a2 == 2:
            a.show_all_attendance()
        elif a2 == 3:
            continue
    elif a1 == 4:
        f = Functions()
        print("1. Add Function.")
        print("2. Show Functions. ")
        print("3. Show Profit/Loss. ")
        print("4. Enter Cost")
        print("5. Back")
        a2 = int(input("Enter your choice: "))
        if a2 == 1:
            valid = 0
            while valid == 0:
                date = input("Date(dd/mm/yyyy): ")
                if validateDate(dob):
                    valid = 1
                else:
                    print("Invalid Date format.!")
            function = input("Enter Function Name: ")
            cost = int(input("Enter Budget: "))
            f.addFunction(date, function, cost)
        elif a2 == 2:
            f.showFunctions()
        elif a2 == 3:
            valid = 0
            while valid == 0:
                date = input("Enter Date(dd/mm/yyyy): ")
                if validateDate(dob):
                    valid = 1
                else:
                    print("Invalid Date format.!")
            f.showPL(date)
        elif a2 == 4:
            valid = 0
            while valid == 0:
                date = input("Date (dd/mm/yyyy): ")
                if validateDate(dob):
                    valid = 1
                else:
                    print("Invalid Date format.!")
            cost = int(input("Enter Cost of Function: "))
            f.spent(date, cost)
        elif a2 == 5:
            continue
    elif a1 == 5:
        break