from pickle import FALSE, TRUE
from statistics import mode
from unittest import defaultTestLoader
from django.contrib.auth.models import User
from django.db import models


class Society(models.Model):
    society_name = models.CharField(max_length=30)
    maintenance_rate = models.IntegerField()

    def __str__(self):
        return str(self.society_name)

class User_Detail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.IntegerField()
    flat = models.CharField(max_length=10)
    user_type = models.SmallIntegerField(null=False, default=1)
    society_name = models.ForeignKey(Society, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

class Event(models.Model):
    society_name = models.ForeignKey(Society, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=100)
    event_description = models.TextField(max_length=500)
    event_start_date = models.DateTimeField()
    event_end_date = models.DateTimeField()

    def __str__(self):
        return str(self.event_name) + ' ' + str(self.event_start_date)

class Complain(models.Model):
    complain_user = models.ForeignKey(User, on_delete=models.CASCADE)
    complain_title = models.CharField(max_length=50)
    complain_type = models.CharField(max_length=15)
    complain_description = models.TextField(max_length=500)
    complain_solution = models.TextField(max_length=500)
    complain_date = models.DateField()
    complain_status = models.BooleanField(null = False, default = False)

    def __str__(self):
        return str(self.complain_user) + ' ' + str(self.complain_title) + ' ' + str(self.complain_type)

class Maintenance(models.Model):
    maintenance_user = models.ForeignKey(User, on_delete=models.CASCADE)
    maintenance_month = models.IntegerField()
    maintenance_year = models.IntegerField()
    payment_date = models.CharField(null=True, max_length=15)

    def __str__(self):
        return str(self.maintenance_user) + ' ' + str(self.maintenance_month) + ' ' + str(self.maintenance_year) + ' ' + str(self.payment_date)

class Contact(models.Model):
    contact_user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_subject = models.CharField(max_length=100)
    contact_description = models.TextField(max_length=500)

    def __str__(self):
        return str(self.contact_user) + ' ' + str(self.contact_subject) + ' ' + str(self.contact_description)
    
