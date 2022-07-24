# from unicodedata import name
from pickle import FALSE, TRUE
from statistics import mode
from django.contrib.auth.models import User
from django.db import models


class Ex_user(models.Model):
    firstname = models.CharField(max_length=50 , null = False , default='default')
    lastname = models.CharField(max_length=50 , null = False , default='default')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.IntegerField( default=1)
    flat = models.CharField(max_length=10 , null=False , default='default')
    society_name = models.CharField(max_length=20 , null=True )

    def __str__(self):
        return str(self.user) + ' ' + str(self.firstname) + ' ' + str(self.lastname)

class Complain(models.Model):
    complain_user = models.ForeignKey(User, on_delete=models.CASCADE)
    complain_name = models.CharField(max_length=50 , null = False , default='default')
    complain_type = models.CharField(max_length=15 , null = False , default='default')
    complain_description = models.CharField(max_length=150 , null = False , default='default')
    complain_solution = models.CharField(max_length=150 , null = False , default='default')
    complain_date = models.DateField()
    complain_status = models.BooleanField(null = False, default = False)

    def __str__(self):
        return str(self.complain_user) + ' ' + str(self.complain_name) + ' ' + str(self.complain_type)

class Maintenance(models.Model):
    maintenance_user = models.ForeignKey(User, on_delete=models.CASCADE)
    maintenance_month = models.DateField()


# MY code goes here

class Contact(models.Model):
      contact_user = models.ForeignKey(User, on_delete=models.CASCADE)
      contact_subject = models.CharField(max_length=30 , null= False , default='deafault')
      contact_description = models.CharField(max_length=200 , null= False , default='deafault')

      def __str__(self):
        return str(self.contact_user) + ' ' + str(self.contact_subject) + ' ' + str(self.contact_description)
    
