from django.forms import ModelForm
from django import forms
from .models import Guest , Department , Entry , Employee , Appointment
from django.contrib.auth.models import User



class GuestForm(ModelForm):
    class Meta:
        model = Guest
        fields = '__all__'



class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = '__all__'
        exclude = ['date' , 'checkOut']



class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'



class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'



class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'



class AppForm(ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'