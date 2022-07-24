from django.contrib import admin
from .models import  User_Detail, Complain , Contact, Society, Event, Maintenance


admin.site.register(User_Detail)
admin.site.register(Complain)
admin.site.register(Contact)
admin.site.register(Society)
admin.site.register(Event)
admin.site.register(Maintenance)