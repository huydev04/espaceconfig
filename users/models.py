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
        userCollection = cndb['User']
        res = userCollection.insert_one(user_data)


    def findUser(Email):
        db = cndb()
        userCollection = db['User']
        query = {'Email' : Email}
        res = userCollection.find_one(query)
        return res

class Post:
    def __init__(self, postID, title, content, imageURL, tags, dateCreated, dateUpdated, status, likesCount, commentsCount, viewsCount, topicID, attachmentID, videoID, voteID):
        self.postID = postID
        self.title = title
        self.content = content
        self.imageURL = imageURL
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
        self.voteID = voteID

    def __str__(self):
        return f"Post(title={self.title}, status={self.status}, likes={self.likesCount})"


class AttachmentFile:
    def __init__(self, AttachmentID, ListFile):
        self.AttachmentID = AttachmentID
        self.listFile = ListFile

class Topic:
    def __init__(self, topicID, topicName):
        self.topicID = topicID
        self.topicName = topicName

class ContentModeration:
    def __init__(self, postID, statusModeration):
        self.postID = postID
        self.statusModeration = statusModeration

class Video:
    def __init__(self, videoID, UrlVideo):
        self.videoID = videoID
        self.UrlVideo = UrlVideo

class Comment:
    def __init__(self, postID, userID, content, date_created, date_updated, reply):
        self.postID = postID
        self.userID = userID
        self.content = content
        self.date_created = date_created
        self.date_updated = date_updated
        self.reply = reply

class Vote:
    def __init__(self, voteID, VoteCount):
        self.voteID = voteID
        self.VoteCount = VoteCount

class ReplyComment:
    def __init__(self, userIDReply, userIDComment, content, dateCreated, dateUpdate):
        self.userIDReply = userIDReply
        self.userIDComment = userIDComment
        self.content = content
        self.dateCreated = dateCreated
        self.dateUpdate = dateUpdate