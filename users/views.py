import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import User, PostDB, AttachmentFile, Topic
from users.source.session import Session
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.template import RequestContext
import os
from django.conf import settings
import datetime
from django.core.management import call_command


# Create your views here.
def login(request):
    if request.method == 'POST':
        Email = request.POST.get('email')
        Password = request.POST.get('password')
        rec = User.findUser(Email)
        print(rec)
        if rec :
            if Password == rec['Password']:
                userID = rec.get('userID')
                FullName = rec.get('FullName')
                DateOfBirth = rec.get('DateOfBirth')
                Gender = rec.get('Gender')
                PhoneNumber = rec.get('PhoneNumber')
                Address = rec.get('Address')
                Country = rec.get('Country')
                ProfilePicture = rec.get('ProfilePicture')
                DateCreated = rec.get('DateCreated')
                Status = rec.get('Status')
                Bio = rec.get('Bio')
                Email = rec.get('Email')
                Password = rec.get('Password')
                Role = rec.get('Role')
                Hash = rec.get('Hash')
                user = User(userID, FullName, DateOfBirth, Gender, PhoneNumber, Address, Country, ProfilePicture, DateCreated, Status, Bio, Email, Password, Role, Hash)
                Session.AddStatusLogin(Session, user)
                Session.getSession(Session)
                return redirect('user:home')
    return render(request, "login_register/login.html")

def Logout(request):
    Session.removeSession(Session)
    return redirect('user:login')

def register(request):
    if request.method == 'POST':
        FullName = request.POST.get('fullname')
        Email = request.POST.get('email')
        DateOfBirth = request.POST.get('dob')
        Gender = request.POST.get('gender')
        PhoneNumber = request.POST.get('phone')
        Address = request.POST.get('address')
        Country = request.POST.get('country')
        Password = request.POST.get('password')
        Password2 = request.POST.get('password2')
        print(Email, Email, Password)
        if not all([FullName, Email, DateOfBirth, Gender, PhoneNumber, Address, Country, Password, Password2]):
            messages.error(request, 'All fields are required.')
        elif Password != Password2:
            messages.error(request, 'Passwords do not match.')
        else:
            try:
                User.addNewUser(User, '', FullName, DateOfBirth, Gender, PhoneNumber, Address, Country, '', '', '', '', Email, Password, 'Member', '')
                messages.success(request, 'Registration successful.')
                return redirect('user:login')
            except Exception as e:
                messages.error(request, f'Error creating user: {e}')
    return render(request, "login_register/register.html")

def home(request):
    if Session.checkStatus(Session) == True:
        listauthor = []
        listuser = User.getListUser()
        listPost = PostDB.listPost()
        topic = Topic.getTopic()
        #listPostTopic = PostDB.topicPost()
        existing_names = set()
        for u in listuser:
            for p in listPost:
                if u.get('FullName') == p.get("author"):
                    author_name = u.get("FullName")
                    if author_name not in existing_names:
                        author = {
                            'name': author_name,
                            'avatar': u.get('ProfilePicture')
                        }
                        listauthor.append(author)
                        existing_names.add(author_name)
        context = {
            'user': Session.getSession(Session),
            'topic': topic,
            'listPost': PostDB.listPost(),
            'authorList': listauthor,
        }
        return render(request, 'homepage/index.html', context)
    else:
        return redirect('user:login')


def profile(request):
    if Session.checkStatus(Session) == True:
        user = Session.getSession(Session)
        listPost = PostDB.getPostOfAuth(user.FullName)
        context = {
            'user': Session.getSession(Session),
            'topic': Topic.getTopic(),
            'listPost': listPost
        }
        return render(request, 'homepage/profile.html', context)
    else:
        return redirect('user:login')


def Post(request):
    if Session.checkStatus(Session) == True:
        context = {
            'user': Session.getSession(Session),
            'topic': Topic.getTopic(),
        }
        return render(request, 'homepage/addpost.html', context)
    else:
        return redirect('user:login')

def Posted(request):
    if Session.checkStatus(Session) == True:

        title = ''
        content = ''
        tags_list = ''
        attachList = ''
        thumbnail = ''
        topic = ''
        attachList = []
        if request.method == 'POST':
            print("POST request received")
            topic = request.POST.get('topicSelect')
            title = request.POST.get('input-name')
            content = request.POST.get('content')
            tags = request.POST.get('postTags')
            listFile = request.FILES.getlist('postFiles')
            thumbnail = request.FILES.get('thumbnail')
            tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()] 
            # Các phần mở rộng của file tài liệu
            document_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']
            # Các phần mở rộng của file media (ảnh)
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            # Các phần mở rộng của file media khác
            media_extensions = image_extensions + ['.mp3', '.mp4', '.avi', '.mov']

            # Lưu hình ảnh thumbnail
            if thumbnail:
                thumbnail_extension = os.path.splitext(thumbnail.name)[1].lower()
                if thumbnail_extension in image_extensions:
                    thumbnail_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
                    if not os.path.exists(thumbnail_dir):
                        os.makedirs(thumbnail_dir)
                    thumbnail_path = os.path.join(thumbnail_dir, thumbnail.name)
                    with open(thumbnail_path, 'wb+') as destination:
                        for chunk in thumbnail.chunks():
                            destination.write(chunk)
                    print(f'Thumbnail saved at: {thumbnail_path}')
                else:
                    print(f'Unsupported thumbnail type: {thumbnail.name}')
            
            # Lưu các file khác
            for file in listFile:
                file_extension = os.path.splitext(file.name)[1].lower()
                if file_extension in document_extensions:
                    # Thư mục đích để lưu trữ file tài liệu
                    upload_dir = os.path.join(settings.MEDIA_ROOT, 'documents')
                elif file_extension in media_extensions:
                    # Thư mục đích để lưu trữ file media
                    upload_dir = os.path.join(settings.MEDIA_ROOT, 'media')
                else:
                    # Nếu loại file không khớp, bỏ qua file này
                    print(f'Unsupported file type: {file.name}')
                    continue

                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)

                file_path = os.path.join(upload_dir, file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                print(f'File saved at: {file_path}')
                attachList.append(file.name)

        attachmentID = AttachmentFile.getID(attachList)
        author = Session.getSession(Session)
        doc = {
                "title": title,
                "content": content,
                "thumbnail": thumbnail.name if thumbnail else None ,
                "tags": tags_list,
                "dateCreated": datetime.datetime.now(),
                "dateUpdated": "",
                "status": "Công khai",
                "topicID": topic,
                "attachmentID": attachmentID,
                "videoID": None,
                "voteCount": 0,
                "likesCount": 0,
                "commentsCount": 0,
                "viewsCount": 0,
                "author": author.FullName,
            }
        PostDB.savePost(doc)
        messages.success(request, 'Đăng bài thành công')
        return redirect('user:home')
    else:
        return redirect('user:login')

def readpage(request):
    title = request.GET.get('param');
    doc = PostDB.getPost(title)
    if doc:
        title = doc['title']
        content = doc['content']
        thumbnail = doc['thumbnail']
        tags = doc['tags'],
        dateCreated = doc['dateCreated']
        dateUpdated = doc['dateUpdated']
        status = doc['status']
        likesCount = doc['likesCount']
        commentsCount = doc['commentsCount']
        viewsCount = doc['viewsCount']
        topicID = doc['topicID']
        attachmentID = doc['attachmentID']
        videoID = doc['videoID']
        voteCount = doc['voteCount']
        author = doc['author']
        attach = AttachmentFile.getAttachFile(attachmentID)
    print(content)
    for i in attach['listFile']:
        print(i)
    context = {
        "title": title,
        "content": content,
        "thumbnail": thumbnail,
        "tags": tags,
        "dateCreated": dateCreated,
        "dateUpdated": dateUpdated,
        "status": status,
        "likesCount": likesCount,
        "commentsCount": commentsCount,
        "viewsCount": viewsCount,
        "topicID": topicID,
        "attachmentID": attachmentID,
        "videoID": videoID,
        "voteCount": voteCount,
        "author": author,
        'topic': Topic.getTopic(),  # Giả sử Topic.getTopic() là một hàm trả về giá trị cho khóa 'topic'
        'listAttach': attach['listFile'],
        'user': Session.getSession(Session),
    }
    return render(request, "homepage/readpage.html", context)


def delete_profile_picture(filename):
    # Define the directory path where the profile pictures are stored
    pp_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'static', 'images', 'avatar'
    )
    # Define the full path to the profile picture
    pp_path = os.path.join(pp_dir, filename)
    
    # Check if the file exists
    if os.path.exists(pp_path):
        # Delete the file
        os.remove(pp_path)
        print(f'Thumbnail deleted: {pp_path}')
    else:
        print(f'Thumbnail not found: {pp_path}')

def account(request):
    if Session.checkStatus(Session) == True:
        u = Session.getSession(Session)
        img_old = u.ProfilePicture if u.ProfilePicture else "avatar.png"
        if request.method == 'GET':
            img_old = request.FILES.get('profilePicture')
        print("old path", img_old)
        if request.method == 'POST':
            full_name = request.POST.get('fullName')
            date_of_birth = request.POST.get('dateOfBirth')
            gender = request.POST.get('gender')
            phone_number = request.POST.get('phoneNumber')
            address = request.POST.get('address')
            country = request.POST.get('country')
            bio = request.POST.get('bio')
            profile_picture = request.FILES.get('profilePicture')
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        # Xử lý file upload
            if profile_picture:
                pp_extension = os.path.splitext(profile_picture.name)[1].lower()
                if pp_extension in image_extensions:
                    # Define the directory path to save the profile picture
                    pp_dir = os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        'static', 'images', 'avatar'
                    )
                    # Create the directory if it doesn't exist
                    if not os.path.exists(pp_dir):
                        os.makedirs(pp_dir)
                    # Define the full path to save the profile picture
                    pp_path = os.path.join(pp_dir, profile_picture.name)
                    # Save the profile picture
                    with open(pp_path, 'wb+') as destination:
                        for chunk in profile_picture.chunks():
                            destination.write(chunk)
                    print(f'Thumbnail saved at: {pp_path}')
                else:
                    print(f'Unsupported thumbnail type: {profile_picture.name}')
            if profile_picture != img_old:
                delete_profile_picture(img_old)
            user = Session.getSession(Session)
            urlprofile = profile_picture.name if profile_picture else None
            User.updateUser(user.userID, full_name, date_of_birth, gender, phone_number, address, country, urlprofile, bio)
            rec = User.findUser(u.Email)
            if rec :
                    userID = rec.get('userID')
                    FullName = rec.get('FullName')
                    DateOfBirth = rec.get('DateOfBirth')
                    Gender = rec.get('Gender')
                    PhoneNumber = rec.get('PhoneNumber')
                    Address = rec.get('Address')
                    Country = rec.get('Country')
                    ProfilePicture = rec.get('ProfilePicture')
                    DateCreated = rec.get('DateCreated')
                    Status = rec.get('Status')
                    Bio = rec.get('Bio')
                    Email = rec.get('Email')
                    Password = rec.get('Password')
                    Role = rec.get('Role')
                    Hash = rec.get('Hash')
                    user = User(userID, FullName, DateOfBirth, Gender, PhoneNumber, Address, Country, ProfilePicture, DateCreated, Status, Bio, Email, Password, Role, Hash)
                    Session.updateSession(Session, user)
            return redirect('user:home')
    else: return redirect('user:login')
    context = {
        'user': Session.getSession(Session),
    }

    return render(request, 'homepage/account.html', context)