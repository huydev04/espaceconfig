from django.db import models
from cn_data import cndb
from datetime import datetime
# Create your models here.

class Admin:
    def __init__(self, username, password, hash_value, full_name, phone_number, role, profile_picture):
        self.username = username
        self.password = password
        self.hash_value = hash_value
        self.full_name = full_name
        self.phone_number = phone_number
        self.role = role
        self.date_created = datetime.now()  # ISO 8601 format
        self.profile_picture = profile_picture

    def findUser(username):
        db = cndb()
        userCollection = db['ac_Admin']
        query = {'Username' : username}
        res = userCollection.find_one(query)
        return res