from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.contrib import messages
from leave_app.models import Form , Number ,Person
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from datetime import datetime
from django.db.models import Sum
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.http import HttpResponseRedirect




# Create your views here.
def home(request) :
    return render(request,"home.html")

def info(request):
    try:
        person=Person.objects.get(username=request.username)
    except Exception as e:
        person = None
        print('Exception : ', e)

    context = {
        'person': person,
    }

    return render(request, 'info.html')

def login(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    #try:
        #   user = Person.objects.get(username=username , password=password)
    #except:
        #   user = None
    user=auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return redirect('/info')
    else:
        messages.info(request, 'Username or Password is incorrect')
        return redirect('/')
    
    
def hr(request):
    return render(request, 'hr.html')

def HRleader(request):
    return render(request, 'HRleader.html')

def leader(request):
    return render(request, 'leader.html')

def createForm(request):
    return render(request, 'createForm.html')

def addForm(request):
    if request.method == "POST":
        username=request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        nickname=request.POST.get('nickname')
        tel=request.POST.get('tel')
        team=request.POST.get('team')
        position=request.POST.get('position')
        email=request.POST.get('email')
        password=request.POST.get('password')
        leader=request.POST.get('leader')
        level=request.POST.get('level')


        person=Person.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            nickname=nickname,
            tel=tel,
            team=team,
            position=position,
            email=email,
            password=password,
            leader=leader,
            level=level
        )
        person.set_password(password)  #แปลงpasswordเป็นการเข้ารหัส
        person.save()
        number = Number.objects.create(username=person)
        number.save()
        
        return render(request, "result.html")

    else:
        return render(request, "createForm.html")
    
def result(request):
    return render(request, 'result.html')

def formleave(request) :
    if request.method == "POST" :
        #รับข้อมูล
        username_id = request.user.id           #ข้อมูลของผู้login
        typeleave = request.POST["typeleave"]
        numberleave = request.POST["numberleave"]
        From_Date = request.POST["From_Date"]
        To_Date = request.POST["To_Date"]
        reason = request.POST["reason"]
        
        #check have day leave
        number_instance = Number.objects.filter(username_id=username_id).first()
        
        if typeleave =='S' :
            form_instance = Form.objects.filter(username_id=username_id,show=0,typeleave='S').aggregate(total_sum=Sum('numberleave'))
            form_sum = form_instance['total_sum'] if form_instance['total_sum'] is not None else 0
            remain = number_instance.sick - form_sum
            if remain < int(numberleave) :
               messages.success(request,"วันลาป่วยของคุณไม่เพียงพอ กรุณากรอกฟอร์มขอลาใหม่อีกครั้ง")
               return redirect('/formleave')        
            
        elif typeleave =='P' :
            form_instance = Form.objects.filter(username_id=username_id,show=0,typeleave='P').aggregate(total_sum=Sum('numberleave'))
            form_sum = form_instance['total_sum'] if form_instance['total_sum'] is not None else 0
            remain = number_instance.personal - form_sum
            if remain < int(numberleave) :
               messages.success(request,"วันลากิจของคุณไม่เพียงพอ กรุณากรอกฟอร์มขอลาใหม่อีกครั้ง")
               return redirect('/formleave')      
           
        else :
            form_instance = Form.objects.filter(username_id=username_id,show=0,typeleave='V').aggregate(total_sum=Sum('numberleave'))
            form_sum = form_instance['total_sum'] if form_instance['total_sum'] is not None else 0
            remain = number_instance.vacation - form_sum
            if remain < int(numberleave) :
               messages.success(request,"วันลาพักร้อนของคุณไม่เพียงพอ กรุณากรอกฟอร์มขอลาใหม่อีกครั้ง")
               return redirect('/formleave')  

        #check number of leave
        date_format = "%Y-%m-%d"
        x = datetime.strptime(From_Date, date_format).date()
        y = datetime.strptime(To_Date, date_format).date()
        difference = y - x
        if int(numberleave) != ((difference.days)+1) :
            messages.success(request,"จำนวนวันลาไม่ถูกต้อง กรุณากรอกฟอร์มขอลาใหม่อีกครั้ง")
            return redirect('/formleave')  
        
        
        #บันทึกข้อมูล
        form = Form.objects.create(
            # name=name,
            # email=email,
            username_id = username_id,
            typeleave=typeleave,
            numberleave=numberleave,
            From_Date = From_Date,
            To_Date = To_Date,
            reason = reason
        )
        form.save()

        leader = request.user.leader
        person_instance = Person.objects.filter(username=leader).first()
        leader_email = person_instance.email
        
        name = request.user.username
        html = render_to_string('emails/contactform.html',{
            'name':name
        })
        
        send_mail('Hi','Hello', 'patinya590@gmail.com' , [leader_email],html_message=html)

        # send email
        # subject = 'Test Email : Leave System'
        # body = '''
        #     <p> เรื่อง ขออนุญาติลา </p>
        #     .......................
        # '''
        # email = EmailMessage(subject=subject , body=body , to=[leader_email])
        # email.content_subtype = 'html'
        # email.send()
        # messages.success(request,"รอการยืนยัน")
        #เปลี่ยนเส้นทาง
        return redirect('/status')        
    return render(request, 'formleave.html') 


def status(request) :
    # if request.method == "POST" :
    username_id = request.user.id 
    all_person = Form.objects.filter(username_id=username_id) 
    all_number = Number.objects.filter(username_id=username_id)
    
    return render(request,"status.html",{"all_person":all_person , "all_number":all_number})

   
def approve(request) :
    username = request.user.username
    allow = Form.objects.filter(username__leader=username,show=0)
    return render(request,"approve.html",{"allow":allow})


def success(request,person_id):
    # เรียกใช้ข้อมูลจากโมเดล Form
    form_instance = Form.objects.get(pk=person_id)
    numberleave_value = form_instance.numberleave
    typeleave_value = form_instance.typeleave
    
    form_instance.show = 1  #เปลี่ยนเป็นTrue
    form_instance.save() 
    
    # เรียกใช้ข้อมูลจากโมเดล Number
    number_instance = Number.objects.filter(username=form_instance.username).first()
    
    if typeleave_value =='S' :
        number_instance.sick -= numberleave_value       
    elif typeleave_value =='P' :
        number_instance.personal -= numberleave_value
    else :
        number_instance.vacation -= numberleave_value
        
    number_instance.save()       
    
    # เรียกใช้ข้อมูลจากโมเดล Person
    person_instance = Person.objects.filter(username=form_instance.username).first()
    person_email = person_instance.email


    subject = 'Test Email'
    body = '''
        <p> mission complete  </p>
    '''
    email = EmailMessage(subject=subject , body=body , to=[person_email])
    email.content_subtype = 'html'
    email.send()
    # messages.success(request,"อนุมัติคำขอของคุณ")
    return redirect("/approve")



def unsuccess(request,person_id) :
    form_instance = Form.objects.get(pk=person_id)
    form_instance.show = 1  #เปลี่ยนเป็นTrue
    form_instance.save() 
    
    # เรียกใช้ข้อมูลจากโมเดล Person
    person_instance = Person.objects.filter(username=form_instance.username).first()
    person_email = person_instance.email
    
    subject = 'Test Email'
    body = '''
        <p> mission fail  </p>
    '''
    email = EmailMessage(subject=subject , body=body , to=[person_email])
    email.content_subtype = 'html'
    email.send()
    # messages.success(request,"ไม่อนุมัติคำขอของคุณ")
    return redirect("/approve")

def logout(request):
    auth.logout(request)
    return redirect('/')