from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import User
# Create your views here.
def login(request):
    if request.method == 'POST':
        Email = request.POST.get('email')
        Password = request.POST.get('password')
        rec = User.getUser(Email)
        print(rec)
        if rec :
            if Password == rec['Password']:
                return redirect('home')
    return render(request, "login_register/login.html")

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
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error creating user: {e}')
    return render(request, "login_register/register.html")

def home(request):
    return render(request, 'homepage/index.html')