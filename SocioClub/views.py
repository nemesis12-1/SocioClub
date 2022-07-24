from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from user_data.models import Maintenance, Society, User_Detail, Complain, Contact
from datetime import date
from django.contrib.auth.decorators import login_required


def index(request):

    if request.user.is_authenticated:
        user_firstname = User.objects.get(username=request.user).first_name
        return render(request, "index.html", {'user_firstname': user_firstname})
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
                return render(request, 'login.html', {'error': 'Record not Valid'})

        elif info.isnumeric():
            phone = info
            if User_Detail.objects.filter(phone=phone).exists():
                user_detail = User_Detail.objects.filter(phone=phone)
                username = user_detail[0].user.username
            else:
                return render(request, 'login.html', {'error': 'Record not Valid'})
        else:
            username = info

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Record not Valid'})

    return render(request, "login.html")


def signup(request):
    society_data = Society.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        phone = request.POST['phone']
        flat = request.POST['flatno']
        society_name = request.POST['society_name']

        fullname = name
        fullname.split()
        firstname = fullname.split()[0]
        lastname = fullname.split()[-1]

        context = {
            'name': name,
            'username': username,
            'email': email,
            'pass1': pass1,
            'phone': phone,
            'flat': flat,
            'society_name': society_name,
        }

        try:
            user = User.objects.get(username=username)
            return render(request, 'signup.html', {'error': 'Username exists', 'context': context, 'society_data': society_data})
        except User.DoesNotExist:
            if User.objects.filter(email=email).exists():
                return render(request, 'signup.html', {'error': 'Email exists', 'context': context, 'society_data': society_data})

            user = User.objects.create_user(
                username=username, password=pass1, email=email, first_name=firstname, last_name=lastname)

            society = Society.objects.get(society_name=society_name) # because One to Many Relation we have to fetch object

            newextendeduser = User_Detail(
                user=user, phone=phone, flat=flat, society_name=society)
            newextendeduser.save()

            auth_user = authenticate(
                request, username=username, password=pass1)
            auth.login(request, auth_user)

            return render(request, "signup.html", {'success': 'Successfully Created Account'})

    return render(request, "signup.html", {'society_data': society_data})


def log_out(request):
    logout(request)
    return redirect('index')


def contact_us(request):
    if request.method == "POST":
        contact_subject = request.POST['contact_subject']
        contact_description = request.POST['contact_description']

        contact = Contact(
            contact_user=request.user,
            contact_subject=contact_subject,
            contact_description=contact_description,
        )

        contact.save()
        return render(request, "contact.html", {'success': True})

    return render(request, "contact.html")


@login_required(login_url='login')
def complain_view(request):
    complains = Complain.objects.filter(complain_user=request.user)
    return render(request, "view-complain.html", {'complains': complains})


@login_required(login_url='login')
def add_complain(request):
    if request.method == "POST":
        print("")
        print("")
        print("")
        print("")
        print("")
        print("YOOOOO")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        complain_title = request.POST['complain_name']
        complain_type = request.POST['complain_type']
        complain_description = request.POST['complain_description']
        complain_solution = request.POST['complain_solution']
        complain_date = date.today()
        complain_status = False

        complain = Complain(
            complain_user=request.user,
            complain_title=complain_title,
            complain_type=complain_type,
            complain_description=complain_description,
            complain_solution=complain_solution,
            complain_date=complain_date,
            complain_status=complain_status,
        )
        complain.save()
        return render(request, "complain.html", {'success': True})

    return render(request, "complain.html")


# @login_required(login_url='login')
def maintenance(request):
    society_name = User_Detail.objects.get(user=request.user).society_name
    return render(request, "maintenance.html", {'society_name':society_name})


# @login_required(login_url='login')
def event(request):
    return render(request, "event.html")


def test(request):
    return render(request, "test.html")
