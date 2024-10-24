from django.shortcuts import render, redirect
from eventapp.models import *
from django.core.serializers import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from eventapp.forms import eventForm
from django.contrib import messages


# Create your views here.

def Admin(request):
    appstaff = list(EventOrganizer.objects.filter(status=True).values_list('user',flat=True))
    if request.user.id in appstaff or request.user.is_superuser:
        if request.user.is_superuser:
            tot = 0
            count = 0
            try:
                t = TicketBooking.objects.all()[:30]
                for i in t:
                    tot += i.total
                    count += i.slots
            except:
                pass
        else:

            tot = 0
            count = 0
            try:
                t = TicketBooking.objects.filter(event__event_organizer__user=request.user)
                for i in t :
                    tot += i.total
                    count += i.slots
            except:
                pass
    else:
        messages.info(request, "you are not approved by admin to access the staff panel")
        return redirect('/')
    return render(request, 'admin.html',{'tot':tot,'count':count})


# Event Tables

def EventList(request):
    event = EventRegister.objects.all().order_by('-id')

    return render(request, 'eventlist.html', {'event': event})


def EventTable(request):
    event = EventRegister.objects.filter(event_organizer__user=request.user)
    print('evenets', event)
    return render(request, 'eventlist.html', {'event': event})


# Activate
def EventActivate(request, id):
    event = EventRegister.objects.get(id=id)
    event.status = True
    event.save()
    messages.info(request, "Event Activated")
    return redirect('evall')


# Deactivate

def EventDeactivate(request, id):
    event = EventRegister.objects.get(id=id)
    event.status = False
    event.save()
    messages.info(request, "Event Deactivated")
    return redirect('evall')


def TicketList(request):
    return render(request, 'ticketlist.html')


def CustomerList(request):
    c = UserRegistration.objects.all()
    return render(request, 'custlist.html',{'c':c})

def confirmedtickets(request):
    tot =0
    slots = 0
    t = TicketBooking.objects.all().order_by('-id')[:30]
    for i in t:
        tot += i.total
        slots += i.slots
    return render(request,'confirmedbookings.html',{'t':t,'tot':tot,'slots':slots})


def EventOrganizerList(request):
    eo = EventOrganizer.objects.all()

    return render(request, 'eventorganizerlist.html', {'key': eo})


def Approve(request, id):
    eo = EventOrganizer.objects.get(id=id)
    eo.status = True
    eo.save()
    messages.info(request, "Organizer Approved")
    return redirect('eoli')


def Depprove(request, id):
    eo = EventOrganizer.objects.get(id=id)
    eo.status = False
    eo.save()
    messages.info(request, "Organizer Deapproved")
    return redirect('eoli')


def LatestEvents(request):
    event = EventRegister.objects.filter(event_organizer__user=request.user)
    return render(request, 'levent.html', {'event': event})


def EditEvent(request, id):
    event = EventRegister.objects.get(id=id)
    f = eventForm(instance=event)
    if request.method == 'POST':
        f = eventForm(instance=event, data=request.POST, files=request.FILES)
        if f.is_valid:
            f.save()
            messages.info(request, "Event Updated")
            return redirect('lev')
    return render(request, 'eventedit.html', {'form': f})


def DeleteEvent(request, id):
    event = EventRegister.objects.get(id=id)
    event.delete()
    messages.info(request, "Event Deleted")
    return redirect('lev')


def LatestBooking(request):
    tot = 0
    slot = 0
    e=0
    t = TicketBooking.objects.filter(event__event_organizer__user=request.user,valid='active')

    print(t)
    for i in t:
        tot += i.total
        slot += i.slots
        e += i.event.slots_available

    return render(request, 'latestbooking.html', {'t': t,'slots':slot,'tot':tot,'e':e})


def VisitedBooking(request):
    tot = 0
    slot = 0
    totc = 0
    slotc = 0
    t = TicketBooking.objects.filter(event__event_organizer__user=request.user,status=True)
    print(t)
    for i in t:
        tot += i.total
        slot += i.slots
    tn =TicketBooking.objects.filter(event__event_organizer__user=request.user,status=False)
    for c in tn:
        totc += c.total
        slotc += c.slots
    return render(request, 'visited.html', {'t': t,'slots':slot,'tot':tot,'tn':tn,'totc':totc,'slotc':slotc})





def TicketVerification(request):
    return render(request, 'jqr.html')


@csrf_exempt
def verify_ticket(request):
    if request.method == 'POST':
        # Decode the request body to extract the decoded text
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        decoded_text = body.get('decodedText')

        # Retrieve ticket details from the database
        try:
            ticket = TicketBooking.objects.get(slug=decoded_text)
            if TicketBooking.objects.filter(slug=decoded_text,status=True,valid='active').exists():
                response_data = {
                    'message': 'Ticket Already verified..!!',
                    'ticket_details': {'ticket_owner':'already visited the event'}
                }
                return JsonResponse(response_data)
            else:
                ticket_details = {
                    'date': ticket.datetime,
                    'ticket_owner': ticket.user.username,
                    'seat': ticket.slots
                }
                # Print the ticket details in the terminal
                print('Ticket Details:', ticket_details)
                ticket.status = True
                ticket.save()
                # Return a JSON response with ticket details
                response_data = {
                    'message': 'Ticket verification successful',
                    'ticket_details': ticket_details
                }
                return JsonResponse(response_data)
        except TicketBooking.DoesNotExist:
            return JsonResponse({'error': 'Ticket not found'}, status=404)
    else:
        # Handle other HTTP methods if needed
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def attendedlist(request):
    ticket = TicketBooking.objects.filter(status=True, event_event_organizer_user=request.user)
    return render(request, 'attend.html', {'tc': ticket})
