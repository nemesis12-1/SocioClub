from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from user_data.models import Maintenance, Society, User_Detail, Complain, Contact, Event, Flatno
from datetime import date, datetime
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

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {'error':'Username exists', 'context':context, 'society_data':society_data})
        elif User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email exists', 'context': context, 'society_data': society_data})      
        else:
            user = User.objects.create_user(username=username, password=pass1, email=email, first_name=firstname, last_name=lastname)
            society = Society.objects.get(society_name=society_name)
            flat_owner = User.objects.get(username=username)
            create_flat = Flatno(flat=flat, society_name=society, owner=flat_owner)
            create_flat.save()
            flat_object = Flatno.objects.get(flat=flat)

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
        if now >= start and now <=end:
            ongoing_event[event] = event.event_name
        elif now<=start:
            upcoming_event[event] = event.event_name

    return render(request, "event.html", {'ongoing_event': ongoing_event, 'upcoming_event': upcoming_event})


def test(request):
    maintenance_data = Maintenance.objects.filter(maintenance_user = request.user).order_by('-maintenance_month')
    return render(request, "test.html", {'maintenance_data': maintenance_data})

def sec_main(request):
    society_name = User_Detail.objects.get(user=request.user).society_name
    maintenance_data = Maintenance.objects.filter(society_name=society_name)
    if request.method == 'POST':

        sec_flat = request.POST['sec_flat']
        maintenance_month = request.POST['sec_month']
        maintenance_year = request.POST['sec_year']
        payment_date = request.POST.get('sec_payment_date')
        

        if Flatno.objects.filter(flat=sec_flat).exists():
            maintenance_user = Flatno.objects.get(flat=sec_flat).owner
            flat = Flatno.objects.get(flat=sec_flat)
            m = Maintenance(
                society_name=society_name, 
                maintenance_user = maintenance_user,
                maintenance_flat = flat,
                maintenance_amount = 5000,
                maintenance_month = maintenance_month, 
                maintenance_year = maintenance_year, 
                payment_date = payment_date
            )
            m.save()
        else:
            return render(request, "sec-main.html", {'maintenance_data': maintenance_data ,'error': 'Flat/Wing Number does not exist'})

    return render(request, "sec-main.html", {'maintenance_data': maintenance_data})

def delete_main(request, id):
    if request.method == 'POST':
        pi = Maintenance.objects.get(pk=id)
        pi.delete()
        return redirect('sec_main')
    return redirect('sec_main')


def update_main(request, id):
    if request.method == 'POST':
        pi = Maintenance.objects.get(pk=id)
        sec_flat = request.POST['sec_flat']
        maintenance_month = request.POST['sec_month']
        maintenance_year = request.POST['sec_year']
        payment_date = request.POST.get('sec_payment_date')

        if Flatno.objects.filter(flat=sec_flat).exists():
            maintenance_user = Flatno.objects.get(flat=sec_flat).owner
            flat = Flatno.objects.get(flat=sec_flat)

            pi.maintenance_user = maintenance_user
            pi.maintenance_flat = flat
            pi.maintenance_month = maintenance_month
            pi.maintenance_year = maintenance_year
            pi.payment_date = payment_date
            pi.save()
        else:
            return render(request, "sec-main.html", {'error': 'Flat/Wing Number does not exist'})
        return redirect('sec_main')
    return redirect('sec_main')


def sec_complain(request):
    society_name = User_Detail.objects.get(user = request.user).society_name
    # complains_data = Complain.objects.filter(complain_user = users_current_society).order_by('-id')
    complains_data = Complain.objects.filter(society_name=society_name).order_by('-complain_date')
    print("")
    print("")
    print(complains_data)
    print("")
    print("")
    return render (request , "sec-complain.html", {'complains':complains_data})


def sec_event(request):
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

    return render (request, "sec-event.html", {'events': events})

def delete_event(request, id):
    if request.method == 'POST':
        if Event.objects.filter(pk=id).exists():
            pi = Event.objects.get(pk=id)
            pi.delete()
            return redirect('sec_event')
        else:
            return redirect('sec_event', {'error': 'No ID'})
    return redirect('sec_event')

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
            print("")
            print("")
            print(pi.event_name)
            print("")
            print(pi.event_description)
            print("")
        return redirect('sec_event')
    return redirect('sec_event')


def user_profile(request):

    return render (request , "user-profile.html")