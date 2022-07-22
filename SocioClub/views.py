from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout

from user_data.models import Ex_user, Complain 
from datetime import date


def index(request):
    return render(request, "index.html")


def login(request):
    if request.method == "POST":
        info = request.POST["info"]
        password = request.POST["password"]

        if '@' in info:
            email = info
            if User.objects.filter(email=email).exists():
                user_detail = User.objects.filter(email=email)
                username = user_detail[0].username
            else:
                 
                #  list = array
                #  abc = [1,"mihir",2,3]

                # dict
                # dict = {'key': 'value', 'key2': 'value'}
                # error = {'Records not valid'}

                return render(request, 'login.html' , {'error': 'Record not Valid'})

                
        elif info.isnumeric():
            phone = info
            if Ex_user.objects.filter(phone=phone).exists():
                user_detail = Ex_user.objects.filter(phone=phone)
                username = user_detail[0].user.username 
            else:
                return render(request, 'login.html' , {'error': 'Record not Valid'})
        else:
            username = info


        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html' , {'error': 'Record not Valid'})

    return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        phone = request.POST['phone']
        flat = request.POST['flatno']
        society_name = request.POST['society_name']

        fullname = name
        fullname.split()
        firstname = fullname.split()[0]
        lastname = fullname.split()[-1]

        context = {
            'name' : name,
            'username': username,
            'email' : email ,
            'pass1' : pass1,
            'phone' : phone,
            'flat' : flat,
            'society_name' : society_name,
        }

        try:
            user = User.objects.get(username=username)
            return render(request, 'signup.html', {'error': 'Username exists', 'context': context})
        except User.DoesNotExist:
            if User.objects.filter(email=email).exists():
                return render(request, 'signup.html', {'error': 'Email exists', 'context': context})

            user = User.objects.create_user(
                username=username, password=pass1, email=email)
            newextendeduser = Ex_user(
                firstname=firstname, lastname=lastname, phone=phone, flat=flat, society_name=society_name, user=user)
            newextendeduser.save()

            auth_user = authenticate(request, username=username, password=pass1)
            auth.login(request, auth_user)

            return render(request, "signup.html", {'success': 'Successfully Created Account'})

    return render(request, "signup.html")

def log_out(request):
    logout(request)
    return redirect('index')

def contact_us(request):
    # if request.method == "POST":
    #      contact_name = request.POST['complain_name']
    #      contact_description = request.POST['complain_name']


    #      contact = Contact(
    #         contact_name = contact_name,
    #         contact_description = contact_description,
    #      )

    #      contact.save
    #      return render(request, "contact.html" , {'success': True})

    return render(request, "contact.html")


def complain_view(request):
    complains = Complain.objects.filter(complain_user=request.user)
    return render(request, "view-complain.html", {'complains': complains})


def add_complain(request):
    if request.method == "POST":
        complain_name = request.POST['complain_name']
        complain_type = request.POST['complain_type']
        complain_description = request.POST['complain_description']
        complain_solution = request.POST['complain_solution']
        complain_date = date.today()
        complain_status = False

        complain = Complain(
            complain_user=request.user,
            complain_name=complain_name,
            complain_type=complain_type,
            complain_description=complain_description,
            complain_solution=complain_solution,
            complain_date=complain_date,
            complain_status=complain_status,
        )
        complain.save()
        return render(request, "complain.html", {'success': True})
        
    return render(request, "complain.html")


def maintenance(request):
    return render(request, "maintenance.html")


def test(request):
    return render(request, "test.html")
