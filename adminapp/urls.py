from django.urls import path
from adminapp import views

urlpatterns = [
    path('',views.Admin,name='nad'),
    path('eventlistall',views.EventList,name='evall'),
    path('eventli',views.EventTable,name='evl'),
    path('eventact/<int:id>/',views.EventActivate,name='aei'),
    path('eventdeact/<int:id>/',views.EventDeactivate,name='adi'),
    path('ticketli',views.TicketList,name='til'),
    path('custli',views.CustomerList,name='cil'),
    path('eorganli',views.EventOrganizerList,name='eoli'),
    path('approve/<int:id>/',views.Approve,name='appr'),
    path('depprove/<int:id>/',views.Depprove,name='deppr'),
    path('ticketverifcation',views.TicketVerification,name='tckv'),
    path('verify_ticket/', views.verify_ticket, name='vt'),
    path('latestevents',views.LatestEvents,name='lev'),
    path('eventedit/<int:id>/',views.EditEvent,name='eedit'),
    path('delevent/<int:id>/',views.DeleteEvent,name='delev'),
    path('latestbok',views.LatestBooking,name='lbok'),
    path('visited',views.VisitedBooking,name='visted'),
    path('confbook',views.confirmedtickets,name='cbt'),
]
