from cn_data import cndb
import random
import string
import bson
from bson.objectid import ObjectId
from django.db import models

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
        self.Hash = Hash


    def generate_random_numeric_string(length=10):
        digits = string.digits
        random_string = ''.join(random.choice(digits) for i in range(length))
        return random_string


    def addNewUser(self,userID, FullName, DateOfBirth, Gender, PhoneNumber, Address, Country, ProfilePicture, DateCreated, Status, Bio, Email, Password, Role, Hash):
        user_data = {
            "userID": self.generate_random_numeric_string(),
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
        res = userCollection.insert_one(user_data)


    def findUser(Email):
        db = cndb()
        userCollection = db['User']
        query = {'Email' : Email}
        res = userCollection.find_one(query)
        return res
    
    def getListUser():
        db = cndb()
        userCollection = db['User']
        res = userCollection.find({})
        return res

    def updateUser(userID, FullName, DateOfBirth, Gender, PhoneNumber, Address, Country, ProfilePicture, Bio):
        db = cndb()
        userCollection = db['User']
        filter = {'userID': userID}
        update = {
            '$set':{
                "FullName": FullName,
                "DateOfBirth": DateOfBirth,
                "Gender": Gender,
                "PhoneNumber": PhoneNumber,
                "Address": Address,
                "Country": Country,
                "ProfilePicture": ProfilePicture,
                "Bio": Bio,
            }
        }
        result = userCollection.update_one(filter, update)


class PostDB:
    def __init__(self, title, content, thumbnail, tags, dateCreated, dateUpdated, status, likesCount, commentsCount, viewsCount, topicID, attachmentID, videoID, voteCount, author):
        self.title = title
        self.content = content
        self.thumbnail = thumbnail
        self.tags = tags
        self.dateCreated = dateCreated
        self.dateUpdated = dateUpdated
        self.status = status
        self.likesCount = likesCount
        self.commentsCount = commentsCount
        self.viewsCount = viewsCount
        self.topicID = topicID
        self.attachmentID = attachmentID
        self.videoID = videoID
        self.voteCount = voteCount
        self.author = author

    def savePost(doc):
        db = cndb()
        postCollection = db['Post']
        print("Gọi savePost")
        result = postCollection.insert_one(doc)
        inserted_id = result.inserted_id
        ContentModeration = db['ContentModeration']
        checkRec = {
            'topicID': inserted_id,
            'statusModeration': "Accept"
        }
        check = ContentModeration.insert_one(checkRec)

    def listPost():
        db = cndb()
        postCollection = db['Post']
        print("Gọi listPost")
        getList = postCollection.find({})
        return getList
    
    def getPost(title):
        db = cndb()
        postCollection = db['Post']
        print("Gọi getPost")
        getPost = postCollection.find_one({"title": title})
        return getPost
    
    def getPostOfAuth(author):
        db = cndb()
        postCollection = db['Post']
        print("Gọi listPost")
        getList = postCollection.find({'author': author})
        return getList
    def topicPost(topicID):
        db = cndb()
        postCollection = db['Post']
        getList = postCollection.find({"topicID": Topic})
        return getList

    def __str__(self):
        return f"Post(title={self.title}, status={self.status}, likes={self.likesCount})"


class AttachmentFile:
    def __init__(self, ListFile):
        self.listFile = ListFile
    
    def getID(attachList):
        db = cndb()
        attachmentFileCollection = db["AttachmentFile"]
        attach_list = {
            'listFile': attachList
        }
        saveAttach = attachmentFileCollection.insert_one(attach_list)
        latest_document = attachmentFileCollection.find().sort('_id', -1).limit(1)
        attachmentID = ""
        for doc in latest_document:
            attachmentID = doc['_id']
        return attachmentID
    
    def getAttachFile(attachmentID):
        db = cndb()
        attachmentFileCollection = db["AttachmentFile"]
        get = attachmentFileCollection.find_one({'_id': attachmentID})
        return get

class Topic:
    def __init__(self, topicID, topicName):
        self.topicID = topicID
        self.topicName = topicName

    def getTopic():
        db = cndb()
        topic = db['Topics']
        rec = topic.find({})
        for topic in rec:
            return topic

    def findTopic(p):
        db = cndb()
        topic = db['Topics']
        rec = topic.find({'topID': p})
        return rec


class ContentModeration:
    def __init__(self, postID, statusModeration):
        self.postID = postID
        self.statusModeration = statusModeration

class Video:
    def __init__(self, videoID, UrlVideo):
        self.videoID = videoID
        self.UrlVideo = UrlVideo

class Comment:
    def __init__(self, titlePost, userName, content, date_created, date_updated, reply):
        self.titlePost = titlePost
        self.userName = userName
        self.content = content
        self.date_created = date_created
        self.date_updated = date_updated
        self.reply = reply
    
    def receive(self, titlePost, userName, content, date_created, date_updated, reply):
        db = cndb()
        Comment = db['Comments']
        doc = {

        }
        


class ReplyComment:
    def __init__(self, userIDReply, userIDComment, content, dateCreated, dateUpdate):
        self.userIDReply = userIDReply
        self.userIDComment = userIDComment
        self.content = content
        self.dateCreated = dateCreated
        self.dateUpdate = dateUpdate
 