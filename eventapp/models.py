import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
roles = (('none', 'None'), ('female', 'Female'), ('male', 'Male'), ('other', "Other"))


class UserRegistration(models.Model):
    username = models.CharField(max_length=20)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    gender = models.CharField(max_length=20, choices=roles)
    dob = models.DateField(default=datetime.date.today)
    city = models.CharField(max_length=50, default='')
    district = models.CharField(max_length=120, default='')
    pincode = models.CharField(max_length=6, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.username


class EventOrganizer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    organization = models.CharField(max_length=100)
    manager = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.organization


class EventRegister(models.Model):
    event_organizer = models.ForeignKey(EventOrganizer, on_delete=models.CASCADE, null=True, default=1)
    event_name = models.CharField(max_length=100)
    event_image = models.ImageField(upload_to='event_images')
    description = models.TextField()
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    ticket_price = models.PositiveIntegerField()
    slots_available = models.PositiveIntegerField(null=True)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    place = models.CharField(max_length=200)
    focus = models.CharField(max_length=20, choices=roles)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.event_name


class TicketBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(EventRegister, on_delete=models.CASCADE)
    qrcode = models.ImageField(upload_to='ticket_qrcode')
    slots = models.PositiveIntegerField(null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    total = models.PositiveIntegerField(null=True)
    slug = models.SlugField(max_length=8, unique=True, null=True)
    status = models.BooleanField(default=False)
    valid = models.CharField(max_length=20, choices=(('active', 'Active'), ('expired', 'Expired')), default='active')

    def __str__(self):
        return self.user.username
