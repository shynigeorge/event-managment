from django.urls import path
from eventapp import views

urlpatterns = [
    path('',views.Home,name='homepage'),
    path('register',views.Register,name='registerpage'),
    path('login',views.LoginFunction,name='loginpage'),
    path('logout',views.LogoutFunction,name='logoutpage'),
    path('eventregister',views.Event_Register,name='eventpage'),
    path('eventdescr/<int:id>/',views.eventdescr,name='eventdescription'),
    path('organregister',views.OrganizerRegister,name='orgreg'),
    path('organlist',views.ApprovePage,name='orglist'),
    path('active/<int:aid>/',views.activefun,name='active'),
    path('deactive/<int:aid>/',views.deactive,name='deactive'),
    path('ticketbook/<int:id>/<int:slots>/<int:total>/',views.Ticket_booking,name='tk'),
    path('ticketdownload/<int:id>/',views.TicketCreation,name='tc'),
    path('debitccard/<int:id>/<int:slots>/<int:total>/',views.debitcard,name='debt'),
    path('payment/<int:id>/<int:slots>/<int:total>/',views.paymentconfirm,name='pay'),
    path('myticket',views.Myticket,name='mytk'),
    path('ticketdel/<int:id>/',views.ticketdelete,name='tdel'),
    path('search',views.search,name='search'),



]