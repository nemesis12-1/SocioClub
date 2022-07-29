from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from user_data.models import Maintenance, Society, User_Detail, Complain, Contact, Event, Flatno
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
import time


def index(request):

    if request.user.is_authenticated:
        user_firstname = User.objects.get(username=request.user).first_name
        user_type = User_Detail.objects.get(user=request.user)

        return render(request, "index.html", {'user_firstname': user_firstname, 'user_type': user_type})
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

        society = Society.objects.get(society_name=society_name)
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {'error':'Username exists', 'context':context, 'society_data':society_data})
        elif User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email exists', 'context': context, 'society_data': society_data})   
        elif User_Detail.objects.filter(phone=phone).exists():
            return render(request, 'signup.html', {'error': 'Phone No Already Exists', 'context': context, 'society_data': society_data})   
        elif Flatno.objects.filter(flat=flat, society_name=society).exists():
            return render(request, 'signup.html', {'error': 'Flat No Already Exists', 'context': context, 'society_data': society_data})   
        else:
            user = User.objects.create_user(username=username, password=pass1, email=email, first_name=firstname, last_name=lastname)
            flat_owner = User.objects.get(username=username)
            create_flat = Flatno(flat=flat, society_name=society, owner=flat_owner)
            create_flat.save()
            flat_object = Flatno.objects.get(flat=flat, society_name=society)

            user_details = User_Detail(user=user,phone=phone,flat=flat_object,society_name=society)
            user_details.save()

            auth_user = authenticate(request, username=username, password=pass1)
            auth.login(request, auth_user)

            return render(request, "signup.html", {'success': 'Successfully Created Account'})     

    return render(request, "signup.html", {'society_data': society_data})


def log_out(request):
    logout(request)
    return redirect('index')


def contact_us(request):
    user_type = None
    if request.user.is_authenticated:
        user_type = User_Detail.objects.get(user=request.user)
    if request.method == "POST":
        contact_subject = request.POST['contact_subject']
        contact_description = request.POST['contact_description']

        contact = Contact(
            contact_user=request.user,
            contact_subject=contact_subject,
            contact_description=contact_description,
        )

        contact.save()
        return render(request, "contact.html", {'success': True, 'user_type': user_type})

    return render(request, "contact.html", {'user_type':user_type})


@login_required(login_url='login')
def complain_view(request):
    complains = Complain.objects.filter(complain_user=request.user).order_by('-id')[:10]
    return render(request, "view-complain.html", {'complains': complains})


@login_required(login_url='login')
def add_complain(request):
    if request.method == "POST":
        society_name = User_Detail.objects.get(user=request.user).society_name
        complain_title = request.POST['complain_name']
        complain_type = request.POST['complain_type']
        complain_description = request.POST['complain_description']
        complain_solution = request.POST['complain_solution']
        complain_date = date.today()
        complain_status = False
        flat = Flatno.objects.get(owner=request.user)

        complain = Complain(
            society_name = society_name,
            complain_user=request.user,
            flat=flat,
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


@login_required(login_url='login')
def maintenance(request):
    maintenance_data = Maintenance.objects.filter(maintenance_user = request.user).order_by('-maintenance_month')
    society_name = User_Detail.objects.get(user=request.user).society_name
    return render(request, "maintenance.html", {'society_name': society_name, 'maintenance_data': maintenance_data})


@login_required(login_url='login')
def event(request):
    society_name = User_Detail.objects.get(user=request.user).society_name
    events = Event.objects.filter(society_name = society_name)
    current_date = datetime.now()

    ongoing_event = {}
    upcoming_event = {}

    now = current_date.strftime("%d/%m/%Y %H:%M")

    for event in events:
        start = event.event_start_date.strftime("%d/%m/%Y %H:%M")
        end = event.event_end_date.strftime("%d/%m/%Y %H:%M")
        if time.strptime(now, "%d/%m/%Y %H:%M") >= time.strptime(start, "%d/%m/%Y %H:%M") and time.strptime(now, "%d/%m/%Y %H:%M") <= time.strptime(end, "%d/%m/%Y %H:%M"):
            ongoing_event[event] = event.event_name
        elif time.strptime(now, "%d/%m/%Y %H:%M") <= time.strptime(start, "%d/%m/%Y %H:%M"):
            upcoming_event[event] = event.event_name

    return render(request, "event.html", {'ongoing_event': ongoing_event, 'upcoming_event': upcoming_event})


@login_required(login_url='login')
def sec_main(request):
    user_type = User_Detail.objects.get(user=request.user)
    if user_type.user_type == 1:
        return redirect('index')
    society_name = User_Detail.objects.get(user=request.user).society_name
    society_amount = Society.objects.get(society_name=society_name).maintenance_rate
    maintenance_data = Maintenance.objects.filter(society_name=society_name).order_by('-id')

    if request.method == 'POST':
        sec_flat = request.POST['sec_flat']
        maintenance_month = request.POST['sec_month']
        maintenance_year = request.POST['sec_year']
        maintenance_amount = request.POST['sec_amount']
        payment_date = request.POST.get('sec_payment_date')
        

        if Flatno.objects.filter(flat=sec_flat, society_name=society_name).exists():
            maintenance_user = Flatno.objects.get(flat=sec_flat, society_name = society_name).owner
            flat = Flatno.objects.get(flat=sec_flat, society_name = society_name)
            m = Maintenance(
                society_name=society_name, 
                maintenance_user = maintenance_user,
                maintenance_flat = flat,
                maintenance_amount = maintenance_amount,
                maintenance_month = maintenance_month, 
                maintenance_year = maintenance_year, 
                payment_date = payment_date
            )
            m.save()
        else:
            return render(request, "sec-main.html", {'maintenance_data': maintenance_data ,'error': 'Flat/Wing Number does not exist', 'user_type':user_type, 'society_amount':society_amount})

    return render(request, "sec-main.html", {'maintenance_data': maintenance_data, 'user_type':user_type, 'society_amount':society_amount})

@login_required(login_url='login')
def delete_main(request, id):
    if request.method == 'POST':
        pi = Maintenance.objects.get(pk=id)
        pi.delete()
        return redirect('sec_main')
    return redirect('sec_main')


@login_required(login_url='login')
def update_main(request, id):
    if request.method == 'POST':
        pi = Maintenance.objects.get(pk=id)
        sec_flat = request.POST['sec_flat']
        maintenance_month = request.POST['sec_month']
        maintenance_year = request.POST['sec_year']
        payment_date = request.POST.get('sec_payment_date')

        society_name = User_Detail.objects.get(user=request.user).society_name

        if Flatno.objects.filter(flat=sec_flat, society_name = society_name).exists():
            maintenance_user = Flatno.objects.get(flat=sec_flat, society_name = society_name).owner
            flat = Flatno.objects.get(flat=sec_flat, society_name = society_name)

            pi.maintenance_user = maintenance_user
            pi.maintenance_flat = flat
            pi.maintenance_month = maintenance_month
            pi.maintenance_year = maintenance_year
            pi.payment_date = payment_date
            pi.save()
        else:
            return redirect('sec_main', {'error': 'Flat/Wing Number does not exist'})
        return redirect('sec_main')
    return redirect('sec_main')

@login_required(login_url='login')
def sec_complain(request):
    user_type = User_Detail.objects.get(user=request.user)
    if user_type.user_type == 1:
        return redirect('index')
    society_name = User_Detail.objects.get(user = request.user).society_name
    complains_data = Complain.objects.filter(society_name=society_name).order_by('-id')
    return render (request , "sec-complain.html", {'complains':complains_data, 'user_type':user_type})

@login_required(login_url='login')
def update_complain(request, id):
    if request.method == 'POST':
        complain_solution = request.POST['complain_solution']

        pi = Complain.objects.get(pk=id)

        pi.complain_solution = complain_solution
        pi.save()

        return redirect('sec_complain')
    return redirect('sec_complain')


@login_required(login_url='login')
def sec_event(request):
    user_type = User_Detail.objects.get(user=request.user)
    if user_type.user_type == 1:
        return redirect('index')
    society_name = User_Detail.objects.get(user=request.user).society_name
    events = Event.objects.filter(society_name = society_name).order_by('-event_start_date')

    if request.method == 'POST':
        event_name = request.POST['event_name']
        event_description = request.POST['event_description']
        event_start_date = request.POST['event_start_date']
        event_end_date = request.POST['event_end_date']
        event_start = datetime.strptime(event_start_date, '%Y-%m-%dT%H:%M')
        event_end = datetime.strptime(event_end_date, '%Y-%m-%dT%H:%M')
  
        sec_event_var = Event(
            society_name=society_name, 
            event_name=event_name, 
            event_description=event_description, 
            event_start_date = event_start, 
            event_end_date=event_end
        )
        sec_event_var.save()

    return render (request, "sec-event.html", {'events': events, 'user_type':user_type})


@login_required(login_url='login')
def delete_event(request, id):
    if request.method == 'POST':
        if Event.objects.filter(pk=id).exists():
            pi = Event.objects.get(pk=id)
            pi.delete()
            return redirect('sec_event')
        else:
            return redirect('sec_event', {'error': 'No ID'})
    return redirect('sec_event')


@login_required(login_url='login')
def update_event(request, id):
    if request.method == 'POST':
        if Event.objects.filter(pk=id).exists():
            pi = Event.objects.get(pk=id)
            pi.event_name = request.POST['event_name']
            pi.event_description = request.POST['event_description']
            event_start = request.POST['event_start_date']
            event_end = request.POST['event_end_date']
            pi.event_start_date = datetime.strptime(event_start, '%Y-%m-%dT%H:%M')
            pi.event_end_date = datetime.strptime(event_end, '%Y-%m-%dT%H:%M')
            pi.save()
        return redirect('sec_event')
    return redirect('sec_event')


@login_required(login_url='login')
def user_profile(request):
    user_type = User_Detail.objects.get(user=request.user)
    society_name = User_Detail.objects.get(user=request.user).society_name
    phone = User_Detail.objects.get(user = request.user).phone
    flat_no =User_Detail.objects.get(user = request.user).flat
    if request.method == 'POST':
        user_name = request.POST.get('user-profile-name')
        user_email = request.POST.get('user-profile-email')
        user_phone = request.POST.get('user-profile-phone')
        password = request.POST.get('confirm-password')
        matchpass = check_password(password, request.user.password)
        if User.objects.filter(email=user_email).exists():
            email = User.objects.get(username=request.user).email
            if User.objects.get(email=user_email).email != email:
                return render( request , "user-profile.html" ,{'email_error':'Email Already Exists', 'society_name': society_name , 'phone': phone, 'flat_no': flat_no, 'user_type':user_type })
        if User_Detail.objects.filter(phone=user_phone).exists() and User_Detail.objects.get(user=request.user).phone != phone:
                return render( request , "user-profile.html" ,{'phone_error':'Phone Number Already Exists', 'society_name': society_name , 'phone': phone, 'flat_no': flat_no, 'user_type':user_type })
        if matchpass:
            fullname = user_name
            fullname.split()
            firstname = fullname.split()[0]
            lastname = fullname.split()[-1]

            user = User.objects.get(id=request.user.id)
            user.first_name = firstname
            user.last_name = lastname
            user.email = user_email
            user_details = User_Detail.objects.get(user=request.user)
            user_details.phone = user_phone

            user.save()
            user_details.save()
        else:
            return render( request , "user-profile.html" ,{'pass_error':'Password is incorrect', 'society_name': society_name , 'phone': phone, 'flat_no': flat_no, 'user_type':user_type })
        return redirect('user_profile')
    return render( request , "user-profile.html" ,{'society_name': society_name , 'phone': phone, 'flat_no': flat_no, 'user_type':user_type })


@login_required(login_url='login')
def delete_account(request):
    if request.method == 'POST':
        delete_user = User.objects.get(username=request.user)
        delete_user.delete()
    return redirect('index')