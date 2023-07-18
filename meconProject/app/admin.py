from django.contrib import admin

# Register your models here.
from .models import Guest , Entry , Department, Employee,Appointment

admin.site.register(Guest)
admin.site.register(Entry)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Appointment)