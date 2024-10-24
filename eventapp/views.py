import os
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from Event_management_project import settings
from eventapp.models import *
from django.core.mail import EmailMessage
import random
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib import messages
from datetime import date, datetime
from django.utils import timezone


def filter_expired_objects():
    # Get the current date
    current_date = date.today()
    # Filter objects where the expiry_date is less than the current date
    expired_objects = EventRegister.objects.filter(end_date__lt=current_date)
    for i in expired_objects:
        i.status = False
        i.save()
    print(expired_objects)
    tk = TicketBooking.objects.filter(event__end_date__lt=current_date)
    for k in tk:
        k.valid = 'expired'
        k.save()
    print(tk)
    return 'cleared expired events'

    # Now you have the queryset of expired objects


# Create your views here.
def Home(request):
    current_datetime = timezone.now()
    autoclearevent = filter_expired_objects()
    print(autoclearevent)
    upcoming_objects = EventRegister.objects.filter(start_date__gte=current_datetime)
    events = upcoming_objects.order_by('start_date')
    return render(request, 'index.html', {'event': events})


def Register(request):
    if request.method == 'POST':
        uname = request.POST['username']
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        gender = request.POST['gender']
        dob = request.POST['dob']
        city = request.POST['city']
        district = request.POST['district']
        pincode = request.POST['pincode']
        if password == cpassword:
            user = User.objects.create_user(first_name=fname, last_name=lname, email=email, password=password,
                                            username=uname)
            user.save()
            reg = UserRegistration(username=uname, user=user, first_name=fname, last_name=lname,
                                   email=email, gender=gender, dob=dob,
                                   pincode=pincode, city=city, district=district, mobile=mobile)
            reg.save()
            return HttpResponse("Regestration succesffully")
    return render(request, 'event_register.html')


#  For registering an event organizer

def OrganizerRegister(request):
    if request.method == "POST":
        org = request.POST['organ']
        uname = request.POST['uname']
        manager = request.POST['mng']
        email = request.POST['email']
        phone = request.POST['phone']
        pw = request.POST['pw']
        cpw = request.POST['cpw']
        if pw == cpw:

            if User.objects.filter(username=uname).exists():
                print('User already exists')
            else:
                user = User.objects.create_user(username=uname, email=email, password=pw, is_staff=True)
                user.save()
                organizer = EventOrganizer(user=user, organization=org, manager=manager, email=email, phone=phone,
                                           status=False)
                organizer.save()
                return redirect('/')
        else:
            print('password not matching')
            return redirect('/')
    return render(request, 'organizer_register.html')


# Approval Page

def ApprovePage(request):
    data = EventOrganizer.objects.all()
    return render(request, 'organiserlist.html', {'d': data})


# Function for activating

def activefun(request, aid):
    data = EventOrganizer.objects.get(id=aid)
    data.status = True
    data.save()
    return redirect('orglist')


def deactive(request, aid):
    data = EventOrganizer.objects.get(id=aid)
    data.status = False
    data.save()
    return redirect('orglist')


# Login function

def LoginFunction(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logined..!")
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "Login Successfully..!!")
                if request.user.is_superuser:
                    return redirect('nad')
                elif request.user.is_staff:
                    s = EventOrganizer.objects.get(user=user)
                    if s.status == True:
                        return redirect('nad')
                    else:
                        print("You are not approved by the admin")
                        messages.info(request, "You are not approved by the admin to acces staff panel")
                        return redirect('/')
                else:
                    return redirect('/')
            else:
                print('Invalid User')
                messages.info(request, "Invalid Credentials")
        return render(request, 'login.html')


# Logout Function

def LogoutFunction(request):
    logout(request)
    return redirect('loginpage')


@login_required(login_url='loginpage')
def Event_Register(request):
    if request.method == 'POST':
        ename = request.POST['event_name']
        eimg = request.FILES['event_image']
        edesc = request.POST['description']
        stime = request.POST['start_time']
        etime = request.POST['end_time']
        sdate = request.POST['start_date']
        edate = request.POST['end_date']
        tprice = request.POST['ticket_price']
        savl = request.POST['slots_available']
        district = request.POST['district']
        city = request.POST['city']
        place = request.POST['place']
        focus = request.POST['focus']
        eventorganizer = EventOrganizer.objects.get(user=request.user)
        event = EventRegister(event_organizer=eventorganizer, event_name=ename, event_image=eimg, description=edesc,
                              start_time=stime,
                              end_time=etime, start_date=sdate, end_date=edate, ticket_price=tprice,
                              slots_available=savl, district=district, city=city, place=place, focus=focus)
        event.save()
        messages.info(request, "Event Registration Succesfull..!!")
        return redirect('/')

    return render(request, 'eventregister.html')


def search(request):
    query = None
    if request.method == 'GET':
        query = request.GET.get('q')
        event = EventRegister.objects.filter(
            Q(event_name__icontains=query) | Q(district__icontains=query) | Q(
                place__icontains=query) | Q(city__icontains=query) | Q(description__icontains=query) | Q(
                ticket_price__icontains=query) | Q(focus__icontains=query))

        return render(request, 'search.html', {'event': event})
    else:
        return render(request, 'search.html', {})


@login_required(login_url='loginpage')
def eventdescr(request, id):
    a = EventRegister.objects.get(id=id)
    if request.method == 'POST':
        slots = request.POST['slo']
        total = int(slots) * a.ticket_price
        print(total)
        return redirect('debt', id, slots, total)
    return render(request, 'eventdescr.html', {'event': a})


@login_required(login_url='loginpage')
def debitcard(request, id, slots, total):
    if request.method == 'POST':
        return redirect('pay', id, slots, total)
    return render(request, 'debitcard.html')


@login_required(login_url='loginpage')
def paymentconfirm(request, id, slots, total):
    if request.method == 'POST':
        return redirect('tk', id, slots, total)
    return render(request, 'payment.html', {'tot': total, 'e': id})


# Ticket Booking
import qrcode as qrcode


@login_required(login_url='loginpage')
def Ticket_booking(request, id, slots, total):
    try:
        slug = ''
        event = EventRegister.objects.get(id=id)
        user = request.user
        coun = ''.join([str(random.randint(0, 9)) for i in range(2)])
        slug += f'Ticket holder name : {user}' + f'{event.event_name}{coun}'
        print(slug)
        # Generate QR Code
        img = qrcode.make(slug)

        file_path = os.path.join(
            r"D:\AppleFolder\event management project\event management project\media\ticket_qrcode",
            f'{user.username}{coun}ticket.png')
        img.save(file_path)
        ticket_book = TicketBooking(user=user, event=event, qrcode=file_path, slug=slug, slots=slots, total=total)
        ticket_book.save()
        tb = TicketBooking.objects.get(user=user, event=event, slug=slug)
        tb.event.slots_available -= slots
        tb.event.save()
        tb.save()
        subject = 'Your Ticket has been booked..!!'
        message = render_to_string('emailtemp.html', {'uname': user.username, 'tb': tb})
        email = EmailMessage(
            subject, message, to=[user.email]
        )
        email.content_subtype = 'html'
        email.send()
        messages.info(request, "Ticket Booked Succesfully. Please check you email")
        return redirect('/')
    except:
        messages.info(request, "Ticket Generation Failed..!!")
        return redirect('/')


def TicketCreation(request, id):
    t = TicketBooking.objects.get(id=id)
    return render(request, 'ticket.html', {'t': t})


def Myticket(request):
    t = TicketBooking.objects.filter(user=request.user).order_by('valid')
    return render(request, 'myticket.html', {'t': t})


def ticketdelete(request, id):
    t = TicketBooking.objects.get(id=id)
    t.delete()
    messages.info(request, "Ticket Cancelled")
    return redirect('mytk')
