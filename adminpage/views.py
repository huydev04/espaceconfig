from django.shortcuts import render, redirect
from django.http import HttpResponse
from adminpage.source.session import Session
from .models import Admin


# Create your views here.
def home(request):
    if Session.checkStatus(Session) == True:
        context={
            'session': Session.getSession(Session)
        }
        return render(request, "adminpage/index.html", context)
    else: return redirect('loginadmin')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        Password = request.POST.get('password')
        rec = Admin.findUser(username)
        print(rec)
        if rec :
            if Password == rec['Password']:
                username=rec.get('Username'),
                password= rec.get('Password'),
                hash_value= rec.get('Hash'),
                full_name=rec.get("FullName"),
                phone_number=rec.get('PhoneNumber'),
                role=rec.get('Role'),
                profile_picture=rec.get('ProfilePicture')
                user = Admin(username,password,hash_value, full_name, phone_number, role, profile_picture)
                Session.AddStatusLogin(Session, user)
                return redirect('home')
    return render(request, "login_register/loginadmin.html")

def Logout(request):
    Session.removeSession(Session)
    return redirect('home')
 
def censorship(request):
    return render(request, 'adminpage/censorship.html')