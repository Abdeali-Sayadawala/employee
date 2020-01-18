import pymongo
import datetime
import re
client = pymongo.MongoClient("mongodb://localhost:27017")


class Employee:
    db = client["company"]
    col = db["employee"]
    sal = db["salary"]
    att = db["attendance"]
    def add_employee(self, name, address, status, Dateofbirth, email, mobile):
        i = None
        for x in self.col.find():
            i = x
            eid = x["eid"]
        for i in self.col.find():
            if i["email"] == email and i["Deleted"] == False:
                print("E-mail already Exists.")
                return 0
        emailregex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if (re.search(emailregex, email)):
            pass
        else:
            print("Email Invalid.")
            return 0
        if i == None:
            eid = 1
        else:
            data = self.col.find().sort("eid",-1).limit(1)
            for i in data:
                eid = i["eid"]
                eid = eid + 1
        dict = {"eid":eid,"Name":name, "Address":address, "Status":status, "DateofBirth":Dateofbirth, "email":email, "Mobile":mobile, "Deleted": False}
        self.col.insert_one(dict)
        print("Id of "+str(name)+" is "+str(eid))
        if status == "intern":
            self.sal.insert_one({"eid":eid, "Salary": 7000, "date": datetime.date.today().strftime("%d/%m/%Y")})
        elif status == "GOD":
            self.sal.insert_one({"eid":eid, "Salary": 700000, "date": datetime.date.today().strftime("%d/%m/%Y")})
        elif status == "experienced":
            self.sal.insert_one({"eid":eid, "Salary": 25000, "date": datetime.date.today().strftime("%d/%m/%Y")})
            
    def display_all(self):
        data = None
        for x in self.col.find({}, {"_id":0}):
            data = x
        if data == None:
            print("Id not present.")
            return 0
        data = self.col.find({}, {"_id":0, "Address":0, "DateofBirth":0, "Mobile":0})
        for i in data:
            if i["Deleted"] == True:
                continue
            print("Employee ID: ", i["eid"])
            print("Name: ", i["Name"])
            print("Status: ", i["Status"])
            print("E-mail: ", i["email"])
            print("="*40)

    def display_details(self, eid):
        data = None
        for x in self.col.find({"eid": int(eid)}, {"_id":0}):
            data = x
        if data == None:
            print("Id not present.")
            return 0
        data = self.col.find({"eid": int(eid)}, {"_id":0})
        for i in data:
            if i["Deleted"] == True:
                print("ID deleted.")
                break
            print("Employee ID: ", i["eid"])
            print("Name: ", i["Name"])
            print("Address: ", i["Address"])
            print("Status: ", i["Status"])
            print("DateofBirth: ", i["DateofBirth"])
            print("E-mail: ", i["email"])
            print("Mobile", i["Mobile"])
            print("="*40)

    def remove_entry(self, eid):
        data = None
        for x in self.col.find({"eid": int(eid)}, {"_id":0}):
            data = x
        if data == None:
            print("Id not present.")
            return 0
        for i in self.col.find({"eid": int(eid)}, {"_id":0}):
            if i["Deleted"] == True:
                print("ID already deleted.")
                return 0
        self.col.update_one({"eid": int(eid)},{"$set": {"Deleted": True}})
        print(str(eid)+" removed")

    def update_entry(self, eid):
        data = None
        for x in self.col.find({"eid": int(eid)}, {"_id":0}):
            data = x
        if data == None:
            print("Id not present.")
            return 0
        for i in self.col.find({"eid": int(eid)}, {"_id":0}):
            if i["Deleted"] == True:
                print("ID already deleted.")
                return 0
        self.display_details(eid)
        print("Update your details:")
        name = input("Name: ")
        address = input("Address: ")
        status = input("Status: ")
        dob = input("Date of Birth: ")
        email = input("Email: ")
        mobile = input("Mobile: ")
        emailregex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if (re.search(emailregex, email)) == False:
            print("Invalid Email")
            return 0
        query = {"eid": int(eid)}
        execute = {"$set": {"Name":name, "Address":address, "Status":status, "DateofBirth":dob, "email":email, "Mobile":mobile}}
        self.col.update_one(query, execute)
        if status == "intern":
            self.sal.update_one({"eid":int(eid)}, {"$set" : {"eid":int(eid), "Salary": 7000, "date": datetime.date.today().strftime("%d/%m/%Y")}})
        elif status == "GOD":
            self.sal.update_one({"eid":int(eid)}, {"$set" : {"eid":int(eid), "Salary": 700000, "date": datetime.date.today().strftime("%d/%m/%Y")}})
        elif status == "experienced":
            self.sal.update_one({"eid":int(eid)}, {"$set" : {"eid":int(eid), "Salary": 25000, "date": datetime.date.today().strftime("%d/%m/%Y")}})
        self.display_details(eid)

class Attendance:
    db = client["company"]
    col = db["attendance"]
    emp = db["employee"]
    def mark_attendance(self, eid, present):
        for i in self.col.find({"eid": int(eid)}, {"_id":0}):
            if i["Deleted"] == True:
                print("ID deleted.")
                return 0
        self.col.insert_one({"eid":eid, "present":present, "date":datetime.date.today().strftime("%d/%m/%Y")})
    def show_all_attendance(self):
        for i in self.emp.find():
            if i["Deleted"] == True:
                continue
            print(i["Name"])
            for j in self.col.find({"eid":i["eid"]},{"_id":0}):
                print(str(j["date"])+"----"+str(j["present"]))

class Salary:
    db = client["company"]
    col = db["salary"]
    emp = db["employee"]
    hol = db["holidays"]
    att = db["attendance"]   
    def add_salary(self, eid, amount):
        for i in self.emp.find({"eid": int(eid)}, {"_id":0}):
            if i["Deleted"] == True:
                print("ID deleted.")
                return 0
        self.col.insert_one({"eid":eid, "Salary": amount, "date": datetime.date.today().strftime("%d/%m/%Y")})
    def get_salary(self, eid, date = int(datetime.date.today().strftime("%d")), month = int(datetime.date.today().strftime("%m")), year = int(datetime.date.today().strftime("%Y"))):
        count = 0
        holidays = []
        for i in self.emp.find({"eid": int(eid)}, {"_id":0}):
            if i["Deleted"] == True:
                print("ID deleted.")
                return 0
        for i in self.col.find({"eid":eid},{"_id":0, "eid":0, "salary":0}).sort("_id",-1).limit(1):
            dt = int(i['date'][:2])
        for i in hol.find({"Month":int(datetime.date.today().strftime("%m"))}, {"_id":0}):
            if i["Holiday"] != 0:
                holidays.append(int(i["Day"]))
        for i in self.att.find({"eid":eid},{"_id":0, "eid":0}).limit(dt):
            if int(i['present']) == 1 or int(i["date"][:2]) in holidays:
                count = count + 1
        for i in self.col.find({"eid":eid},{"_id":0, "eid":0, "date":0}):
            sal = int(i["Salary"])
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
        
while True:
    print("1. Employee Management.")
    print("2. Salary Management.")
    print("3. Attendance Management.")
    print("4. Exit.")
    a1 = int(input("Enter your choice: "))
    if a1 == 1:
        e = Employee()
        print("1. Add employee")
        print("2. Display")
        print("3. Display all")
        print("4. Remove")
        print("5. Update")
        print("6. Exit")
        a2 = int(input("Enter your choice: "))
        if a2 == 1:
            name = input("Enter Name: ")
            address = input("Enter Address ")
            dob = input("Date of Birth(dd/mm/yyyy): ")
            status = input("Enter Status: ")
            mobile = input("Enter mobile number: ")
            email = input("Enter your mail: ")
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
            break
    elif a1 == 2:
        s = Salary()
        print("1. Get the current salary of employee.")
        print("2. Exit.")
        a2 = int(input("Enter your choice: "))
        if a2 == 1:
            eid = int(input("Enter ID of employee to get the salary: "))
            s.get_salary(eid)
        elif a2 == 2:
            break
    elif a1 == 3:
        a = Attendance()
        print("1. Mark Attendance")
        print("2. Show Attendance")
        print("3. Exit")
        a2 = int(input("Enter your choice: "))
        if a2 == 1:
            eid = int(input("Enter ID of employee: "))
            present = int(input("Enter status: "))
            a.mark_attendance(eid, present)
        elif a2 == 2:
            a.show_all_attendance()
        elif a2 == 3:
            break
    elif a1 == 4:
        break