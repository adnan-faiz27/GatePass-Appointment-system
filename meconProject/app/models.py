from django.db import models
from django.contrib.auth.models import User
from datetime import date , datetime




class Department(models.Model):
    Name = models.CharField(max_length=20 , blank=True)
    Floor = models.IntegerField(default=0)

    def __str__(self):
        return self.Name
    


class Guest(models.Model):
    firstName = models.CharField(max_length= 30)
    lastName = models.CharField(max_length= 20)
    mobileNo = models.IntegerField()
    email = models.EmailField(max_length= 30 , default='user@gmail.com')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated' , '-created']

    def __str__(self):
        return self.firstName + ' ' + self.lastName
    


class Entry(models.Model):
    guestEntry = models.ForeignKey(Guest, on_delete=models.SET_NULL , null = True) 
    department = models.ForeignKey(Department, on_delete=models.SET_NULL , null = True) 
    purpose = models.TextField(blank=True , max_length=50)
    date = models.DateTimeField()
    checkOut = models.DateTimeField(blank=True , null=True)

    def __str__(self):
        return str(self.date)
    


class Employee(models.Model):
    GENDER_CHOICES = (
    ("M", "male"),
    ("F", "female"),
    ("other", "other"),)

    eid = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL , null = True)
    firstName = models.CharField(max_length= 30)
    lastName = models.CharField(max_length= 20)
    mobileNo = models.IntegerField()
    gender = models.CharField(max_length=9,choices=GENDER_CHOICES,default="M")
    email = models.EmailField(max_length= 30 , default='user@gmail.com')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated' , '-created']

    def __str__(self):
        return str(self.eid)
        

class Appointment(models.Model):
    
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    guest = models.ForeignKey(Guest, on_delete=models.SET_NULL , null = True) 
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL , null = True) 
    date = models.DateField(default=date.today)
    time = models.TimeField(default= current_time)

    def __str__(self):
        return str(self.date)
