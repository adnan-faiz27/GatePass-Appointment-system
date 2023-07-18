from django.shortcuts import render , redirect 
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime
import datetime
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login , logout
from .forms import GuestForm , DepartmentForm , EntryForm, EmployeeForm , AppForm
from .models import Guest , Entry , Department , Employee , Appointment
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template 
import pdfkit




def page(request):
    return render(request , 'index1.html')
    # return redirect('viewEmployee')



def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('page')

    if request.method =="POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User doesnt exist')

        user = authenticate(request , username = username , password = password)
        if user != None:
            login(request , user)
            return redirect('page')

        else:
            messages.error(request  ,"Username or Password incorrect" )


    context = {'page':page}
    return render (request , 'user_form.html' , context)




def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    if request.method =="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request , user)
            return redirect('page')
        else:
            messages.error(request , 'An error occurred during registrations')

    return render(request , 'user_form.html' , {'form':form} )




def logoutPage(request):
    logout(request)
    return redirect('page')




def pdf(context):
    options = {
        'page-size': 'A6',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }
    PATH = 'C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=PATH)
    template = get_template("gate_pass.html")
    html = template.render(context) 
    pdfkit.from_string(html, 'gate_pass1.pdf' , options=options)




def mail(guestName , guest , employeeName , emp , date , time , obj):
    context1 = {
        'obj': "Guest Name",
        'obj1':obj,
        'name': guestName,
        'number': guest.mobileNo,
        'date':date,
        'time':time
    }
    html_content1 = render_to_string("email_template.html" , context1) 
    message1 = strip_tags(html_content1)
    context2 = {
        'obj': "Employee Name",
        'obj1':obj,
        'name':employeeName,
        'number': emp.mobileNo,
        'date':date,
        'time':time
    }
    html_content2 = render_to_string("email_template.html" , context2) 
    message2 = strip_tags(html_content2)
    mail1 = EmailMultiAlternatives(
        "APPOINTMENT",
        message1,
        "settings.EMAIL_HOST_USER",
        [emp.email],
    )
    mail1.attach_alternative(html_content1 , "text/html")
        
    mail2 = EmailMultiAlternatives(
        "APPOINTMENT",
        message2,
        "settings.EMAIL_HOST_USER",
        [guest.email],
    )
    mail2.attach_alternative(html_content2 , "text/html")
    if(obj=="scheduled"):
        day = date[8]+date[9]
        month = date[5]+date[6]
        year = date[0]+date[1]+date[2]+date[3]
        valid=""
        if(day=="30" and (month=="04" | month=="06" | month=="09" | month=="11")):
            day = "01"
            if(month=="11"):
                month = "12"
            else:
                month = month.replace(month[1] , chr(ord(month[1]) + 1))
            print(valid)
            print("valid")
        elif(day=="31"):
            day = "01"
            month = month.replace(month[1] , chr(ord(month[1]) + 1))
        elif(day[1]=="9"):
            day = day.replace(day[0] , chr(ord(day[0]) + 1))
            day = day.replace(day[1] , "0")
            
        else:
            day = day.replace(day[1] , chr(ord(day[1]) + 1))

        valid = year+"-"+month+"-"+day
        context = {
            'obj': "Employee Name",
            'obj1':obj,
            'empName':employeeName,
            'guestName':guestName,
            'empNumber': emp.mobileNo,
            'guestNumber': guest.mobileNo,
            'date':date,
            'time':time,
            'valid':valid
        }
        pdf(context)
        mail2.attach_file('gate_pass1.pdf')

    mail1.send(fail_silently=False)
    mail2.send(fail_silently=False)









@login_required(login_url= 'login')
def createGuest(request):
    form = GuestForm()
    if request.method=='POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            firstName = request.POST.get('firstName')
            lastName = request.POST.get('lastName')
            mobileNo = request.POST.get('mobileNo')
            email = request.POST.get('email')
            Guest.objects.create(
                firstName = firstName,
                lastName = lastName,
                mobileNo = mobileNo,
                email = email
            )
            return redirect('view-guest')
        else:
            return render(request , 'guest_form.html', context)
    context = {'form':form , 'obj':"created" }
    return render(request , 'guest_form.html', context)






@login_required(login_url= 'login')
def createEntry(request):
    form = EntryForm()
    x = datetime.datetime.now()
    guests = Guest.objects.all()
    deps = Department.objects.all()
    if request.method=='POST':
        guest_name = request.POST.get('guestEntry')
        guest = Guest.objects.get(id = guest_name )
        dep_name = request.POST.get('department')
        dep = Department.objects.get(id = dep_name )
        purpose = request.POST.get('purpose')
        Entry.objects.create(
            guestEntry = guest,
            department = dep,
            date = x,
            purpose = purpose
        )
        return redirect('view-entry')
    context = {'form':form , 'guests':guests , 'departments':deps , 'obj':"created"}
    return render(request , 'entry_form.html', context)







@login_required(login_url= 'login')
def createDepartment(request):
    form = DepartmentForm()
    if request.method=='POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            Name = request.POST.get('Name')
            Floor = request.POST.get('Floor')
            Department.objects.create(
                Name = Name,
                Floor = Floor
            )
            return redirect('view-dep')
        else:
            return render(request , 'department_form.html', context)
    context = {'form':form , 'obj':"created"}
    return render(request , 'department_form.html', context)





@login_required(login_url= 'login')
def createEmployee(request):
    form = EmployeeForm()
    if request.method=='POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            eid = request.POST.get('eid')
            dep_name = request.POST.get('department')
            dep = Department.objects.get(id = dep_name )
            firstName = request.POST.get('firstName')
            lastName = request.POST.get('lastName')
            mobileNo = request.POST.get('mobileNo')
            email = request.POST.get('email')
            gender = request.POST.get('gender')
            Employee.objects.create(
                eid = eid,
                department  = dep,
                firstName = firstName,
                lastName = lastName,
                mobileNo = mobileNo,
                email = email,
                gender = gender,
            )
            return redirect('view-employee')
        else:
            return render(request , 'employee_form.html', context)
    context = {'form':form ,'obj':"created"}
    return render(request , 'employee_form.html', context)







@login_required(login_url= 'login')
def createApp(request):
    form = AppForm()
    G = Guest.objects.all()
    E = Employee.objects.all()
    if request.method=='POST':
        form = AppForm(request.POST)
        # if form.is_valid():
        guest_name = request.POST.get('guest')
        guest = Guest.objects.get(id = guest_name )
        employee_name = request.POST.get('employee')
        emp = Employee.objects.get(id = employee_name )
        date = request.POST.get('date')
        time = request.POST.get('time')
        time = time+":00"
        guestName = guest.firstName+ " "+guest.lastName
        employeeName = emp.firstName+ " "+emp.lastName
        Appointment.objects.create(
            guest = guest,
            employee = emp,
            date = date,
            time = time
        )
        mail (guestName , guest , employeeName , emp , date , time , "scheduled")
        
        return redirect('view-app')
    context = {'form':form , 'obj':"created"}
    return render(request , 'app_form.html', context)










@login_required(login_url= 'login')
def viewEmployee(request):
    q = request.GET.get('emp') if request.GET.get('emp') != None else ''
    employees = Employee.objects.filter(
        Q(firstName__icontains = q)|
        Q(lastName__icontains = q) |
        Q(mobileNo__icontains = q) |
        Q(eid__icontains = q)
        )
    employee_count = employees.count()
    context = {'employees':employees , 'employee_count':employee_count}
    return render(request , 'viewEmployee.html' ,context ,  )








@login_required(login_url= 'login')
def updateEmployee(request , pk):
    employee = Employee.objects.get(id = pk)
    form = EmployeeForm(instance=employee)
    if request.method=='POST':
        employee.eid = request.POST.get('eid')
        dep_name = request.POST.get('department')
        dep = Department.objects.get(id = dep_name )
        employee.department = dep
        employee.firstName = request.POST.get('firstName')
        employee.lastName = request.POST.get('lastName')
        employee.mobileNo = request.POST.get('mobileNo')
        employee.email = request.POST.get('email')
        employee.gender = request.POST.get('gender')
        employee.save()
        return redirect('view-employee') 
    context = {'employee' : employee , 'form':form , 'obj':"updated"}
    return render(request , 'employee_form.html' , context) 




@login_required(login_url= 'login')
def deleteEmployee(request , pk):
    employee = Employee.objects.get(id =pk)

    if request.method =="POST":
        employee.delete()
        return redirect('view-employee')
    return render(request , 'delete.html' , {'obj':employee})





@login_required(login_url= 'login')
def viewApp(request):
    if(request.GET.get('ap') == None and request.GET.get('date') == None):
        apps = Appointment.objects.all()
    elif(request.GET.get('ap') != ""):
        q = request.GET.get('ap')
        apps = Appointment.objects.filter(
            Q(guest__firstName__icontains = q)|
            Q(guest__lastName__icontains = q)
        )
    elif (request.GET.get('date') != None):
        date = request.GET.get('date')
        apps = Appointment.objects.filter(
            Q(date__icontains = date)
        )
    app_count = apps.count()
    context = {'apps':apps , 'app_count':app_count}
    return render(request , 'viewApp.html' ,context ,  )



@login_required(login_url= 'login')
def updateApp(request , pk):
    app = Appointment.objects.get(id = pk)
    form = AppForm(instance=app)
    if request.method=='POST':
        guest_name = request.POST.get('guest')
        guest = Guest.objects.get(id = guest_name )
        app.guest = guest
        employee_name = request.POST.get('employee')
        emp = Employee.objects.get(id = employee_name )
        app.employee = emp
        app.date = request.POST.get('date')
        app.time = request.POST.get('time')
        app.time = app.time+":00"
        app.save()
        guestName = guest.firstName+ " "+guest.lastName
        employeeName = emp.firstName+ " "+emp.lastName
        mail (guestName , guest , employeeName , emp , app.date , app.time , "rescheduled")
        return redirect('view-app') 
    context = {'form' : form , 'app':app , 'obj':"updated"}
    return render(request , 'app_form.html' , context)



@login_required(login_url= 'login')
def deleteApp(request , pk):
    app = Appointment.objects.get(id =pk)
    
    if request.method =="POST":
        guestName = app.guest.firstName+ " "+app.guest.lastName
        employeeName = app.employee.firstName+ " "+app.employee.lastName
        mail (guestName , app.guest , employeeName , app.employee , app.date , app.time , "canceled")
        app.delete()
        return redirect('view-app')
    return render(request , 'delete.html' , {'obj':app})




@login_required(login_url= 'login')
def viewDep(request):
    deps = Department.objects.all()
    dep_count = deps.count()
    context = {'deps':deps , 'dep_count':dep_count}
    return render(request , 'viewDep.html' ,context ,  )





@login_required(login_url= 'login')
def updateDep(request , pk):
    dep = Department.objects.get(id = pk)
    form = DepartmentForm(instance=dep)
    if request.method=='POST':
        dep.Name = request.POST.get('Name')
        dep.Floor = request.POST.get('Floor')
        dep.save()
        return redirect('view-dep') 
    context = {'dep' : dep , 'form':form , 'obj':"updated"}
    return render(request , 'department_form.html' , context) 



@login_required(login_url= 'login')
def deleteDep(request , pk):
    dep = Department.objects.get(id =pk)

    if request.method =="POST":
        dep.delete()
        return redirect('view-dep')
    return render(request , 'delete.html' , {'obj':dep})





@login_required(login_url= 'login')
def viewGuest(request):
    q = request.GET.get('g') if request.GET.get('g') != None else ''

    guests = Guest.objects.filter(
        Q(firstName__icontains = q)|
        Q(lastName__icontains = q) |
        Q(mobileNo__icontains = q)
        )
    guest_count = guests.count()
    context = {'guests':guests , 'guest_count':guest_count}
    return render(request , 'viewGuest.html' ,context ,  )





@login_required(login_url= 'login')
def updateGuest(request , pk):
    guest = Guest.objects.get(id = pk)
    form = GuestForm(instance=guest)
    if request.method=='POST':
        guest.firstName = request.POST.get('firstName')
        guest.lastName = request.POST.get('lastName')
        guest.mobileNo = request.POST.get('mobileNo')
        guest.email = request.POST.get('email')
        guest.save()
        return redirect('view-guest') 
    context = {'guest' : guest , 'form':form , 'obj':"updated"}
    return render(request , 'guest_form.html' , context) 


@login_required(login_url= 'login')
def deleteGuest(request , pk):
    guest = Guest.objects.get(id =pk)

    if request.method =="POST":
        guest.delete()
        return redirect('view-guest')
    return render(request , 'delete.html' , {'obj':guest})



@login_required(login_url= 'login')
def viewEntry(request):

    entries = []
    if(request.GET.get('checked')!=None and request.GET.get('ent') == "" and  request.GET.get('date') == "" ):
        entries1 = Entry.objects.all()
        print("hello")
        for obj in entries1:
            if obj.checkOut==None:
                entries.append(obj)


    elif(request.GET.get('ent') != "" and request.GET.get('date') == "" and request.GET.get('checked')==None):
        q = request.GET.get('ent')
        print("hello1")
        entries = Entry.objects.filter(
            Q(guestEntry__firstName__icontains = q)|
            Q(guestEntry__lastName__icontains = q)
        )
        
    elif (request.GET.get('date') != "" and request.GET.get('checked')==None and request.GET.get('ent') ==""):
        date = request.GET.get('date')
        print("hello2")
        entries = Entry.objects.filter(
            Q(date__icontains = date)
        )
        
    elif(request.GET.get('ent') == None and request.GET.get('date') == None and request.GET.get('checked')==None ):
        entries1 = Entry.objects.all()
        print("hello3")
        for obj in entries1:
            if obj.checkOut!=None:
                entries.append(obj) 


    elif(request.GET.get('ent') == "" and request.GET.get('date') == "" and request.GET.get('checked')==None ):
        entries1 = Entry.objects.all()
        print("hello4")
        for obj in entries1:
            if obj.checkOut!=None:
                entries.append(obj)
    


    elif(request.GET.get('ent') != "" and request.GET.get('date') != "" and request.GET.get('checked')!=None ):
        q = request.GET.get('ent')
        date = request.GET.get('date')
        entries1 = Entry.objects.filter(
            Q(guestEntry__firstName__icontains = q) | Q(guestEntry__lastName__icontains = q)
        )
        print("hello5")
        print(entries1[0].date.date())
        print(entries1[0].checkOut)
        print(entries1[1].checkOut)
        for obj in entries1:
            if (obj.checkOut == None and obj.date.date() == date):
                entries.append(obj)
        


    elif(request.GET.get('date') != "" and request.GET.get('checked')==None and request.GET.get('ent') != ""):
        print("hello6")
        q = request.GET.get('ent')
        date = request.GET.get('date')
        entries1 = Entry.objects.filter(
            Q(guestEntry__firstName__icontains = q) | Q(guestEntry__lastName__icontains = q)
        )
        for obj in entries1:
            if obj.checkOut!=None and obj.date.date() == date:
                entries.append(obj)




    elif(request.GET.get('date') == "" and request.GET.get('checked')!=None and request.GET.get('ent') !=""):
        print("hello7")
        q = request.GET.get('ent')
        entries1 = Entry.objects.filter(
            Q(guestEntry__firstName__icontains = q) | Q(guestEntry__lastName__icontains = q)
        )
        for obj in entries1:
            if obj.checkOut==None:
                entries.append(obj)


    elif(request.GET.get('date') != "" and request.GET.get('checked')!= None and request.GET.get('ent') ==""):
        print("hello8")
        date = request.GET.get('date')
        entries1 = Entry.objects.filter(
            Q(date__icontains = date)
        )
        for obj in entries1:
            if obj.checkOut!=None and obj.date.date() == date:
                entries.append(obj)
        
        
    
    context = {'entries':entries}
    return render(request , 'viewEntry.html' ,context ,  )





@login_required(login_url= 'login')
def viewEntryCheck(request , pk):
    entry = Entry.objects.get(id = pk)
    entry.checkOut = datetime.datetime.now()
    entry.save()
    entries = Entry.objects.all()
    context = {'entries':entries }
    return render(request , 'viewEntry.html' ,context ,  )




