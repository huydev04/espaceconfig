from cn_data import cndb
import random
import string
# Create your models here.
class User:
    def __init__(self, userID, FullName, DateOfBirth, Gender, PhoneNumber, Address, Country, ProfilePicture, DateCreated, Status, Bio, Email, Password, Role, Hash):
        self.userID = userID
        self.FullName = FullName
        self.DateOfBirth = DateOfBirth
        self.Gender = Gender
        self.PhoneNumber = PhoneNumber
        self.Address = Address
        self.Country = Country
        self.ProfilePicture = ProfilePicture
        self.DateCreated = DateCreated
        self.Status = Status
        self.Bio = Bio
        self.Email = Email
        self.Password = Password
        self.Role = Role
        self.hash = Hash
    
    def generate_random_numeric_string(length=10):
        digits = string.digits
        random_string = ''.join(random.choice(digits) for i in range(length))
        return random_string
    

    def addNewUser(self, userID, FullName, DateOfBirth, Gender, PhoneNumber, Address, Country, ProfilePicture, DateCreated, Status, Bio, Email, Password, Role, Hash):
        user_data = {
        "userID": self.generate_random_numeric_string(100),
        "FullName": FullName,
        "DateOfBirth": DateOfBirth,
        "Gender": Gender,
        "PhoneNumber": PhoneNumber,
        "Address": Address,
        "Country": Country,
        "ProfilePicture": ProfilePicture,
        "DateCreated": DateCreated,
        "Status": Status,
        "Bio": Bio,
        "Email": Email,
        "Password": Password,
        "Role": Role,
        "Hash": Hash
        }
        db = cndb()
        userCollection = db['User']
        rec = userCollection.insert_one(user_data)
        print(rec)
    
    def getUser(Email):
        db = cndb()
        userCollection = db['User']
        query = {'Email': Email}
        rec = userCollection.find_one(query)
        return rec

