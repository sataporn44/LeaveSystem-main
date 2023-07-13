from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.contrib import messages
from leave_app.models import Form , Number ,Person
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from datetime import datetime
from django.db.models import Sum, Q
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request) :
    return render(request,"home.html")

@login_required(login_url='/')
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

@login_required(login_url='/')
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

        # ตรวจสอบข้อมูลที่รับมาจากฟอร์ม
        if not username:
            messages.error(request, "กรุณากรอกชื่อผู้ใช้งาน")
            return render(request, "createForm.html", {
                'username': username, 'first_name': first_name, 'last_name': last_name,
                'nickname': nickname, 'tel': tel, 'team': team, 'position': position,
                'email': email, 'password': password, 'leader': leader, 'level': level
            })

        # สร้างและบันทึกข้อมูล
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

@login_required(login_url='/')   
def result(request):
    return render(request, 'result.html')

@login_required(login_url='/')
def formleave(request) :
    if request.method == "POST" :
        #รับข้อมูล
        username_id = request.user.id           #ข้อมูลของผู้login
        typeleave = request.POST["typeleave"]
        numberleave = request.POST["numberleave"]
        From_Date = request.POST["From_Date"]
        To_Date = request.POST["To_Date"]
        reason = request.POST["reason"]
        
        date_format = "%d %b %Y"
        From_Date = datetime.strptime(From_Date, date_format).strftime("%Y-%m-%d")
        To_Date = datetime.strptime(To_Date, date_format).strftime("%Y-%m-%d")
        
        existing_form = Form.objects.filter(
        username_id=username_id,
        From_Date__lte=To_Date,  # ตรวจสอบวันที่เริ่มต้นก่อนหรือเท่ากับวันที่สิ้นสุด
        To_Date__gte=From_Date  # ตรวจสอบวันที่สิ้นสุดหลังหรือเท่ากับวันที่เริ่มต้น
        ).first()

        if existing_form:
            # ฟอร์มการลาซ้ำกับวันที่มีอยู่ในช่วงเวลาที่กำหนด
            messages.success(request, "ฟอร์มการลาซ้ำกับวันที่มีอยู่ในช่วงเวลาที่กำหนด")
            return redirect('/formleave')
        
        
        #check have day leave
        number_instance = Number.objects.filter(username_id=username_id).first()
        
        if typeleave =='S' :
            type = 'ลาป่วย'
            form_instance = Form.objects.filter(username_id=username_id,show=0,typeleave='S').aggregate(total_sum=Sum('numberleave'))
            form_sum = form_instance['total_sum'] if form_instance['total_sum'] is not None else 0
            remain = number_instance.sick - form_sum
            leave_remain = number_instance.sick
            if remain < int(numberleave) :
               messages.success(request,"วันลาป่วยของคุณไม่เพียงพอ กรุณากรอกฟอร์มขอลาใหม่อีกครั้ง")
               return redirect('/formleave')        
            
        elif typeleave =='P' :
            type = 'ลากิจ'
            form_instance = Form.objects.filter(username_id=username_id,show=0,typeleave='P').aggregate(total_sum=Sum('numberleave'))
            form_sum = form_instance['total_sum'] if form_instance['total_sum'] is not None else 0
            remain = number_instance.personal - form_sum
            leave_remain = number_instance.personal
            if remain < int(numberleave) :
               messages.success(request,"วันลากิจของคุณไม่เพียงพอ กรุณากรอกฟอร์มขอลาใหม่อีกครั้ง")
               return redirect('/formleave')      
           
        else :
            type = 'ลาพักร้อน'
            form_instance = Form.objects.filter(username_id=username_id,show=0,typeleave='V').aggregate(total_sum=Sum('numberleave'))
            form_sum = form_instance['total_sum'] if form_instance['total_sum'] is not None else 0
            remain = number_instance.vacation - form_sum
            leave_remain = number_instance.vacation
            if remain < int(numberleave) :
               messages.success(request,"วันลาพักร้อนของคุณไม่เพียงพอ กรุณากรอกฟอร์มขอลาใหม่อีกครั้ง")
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
        leader_frist = person_instance.first_name
        leader_last = person_instance.last_name

        formatted_From = datetime.strptime(form.From_Date, "%Y-%m-%d").strftime("%d %b %Y")
        formatted_To = datetime.strptime(form.To_Date, "%Y-%m-%d").strftime("%d %b %Y")
        
        username = request.user.username
        person = Person.objects.filter(username=username)        
        html = render_to_string('emails/contactform.html',{
            'leader_frist':leader_frist,
            'leader_last':leader_last,
            'person':person,
            'type':type,
            'numberleave':numberleave,
            'From_Date':formatted_From,
            'To_Date':formatted_To,
            'reason':reason,
            'leave_remain':leave_remain
        })
        
        send_mail('เรื่อง ขออนุญาติลา','Hello', 'patinya590@gmail.com' , [leader_email],html_message=html)
        return redirect('/status')        
    return render(request, 'formleave.html') 

@login_required(login_url='/')
def edit(request,person_id) :
    if request.method == "POST" :
    #เมื่อมีการส่งข้อมูลมา
        form = Form.objects.get(pk=person_id)     #ดึงข้อมูลประชากรที่ต้องการแก้ไข
        form.typeleave = request.POST["typeleave"]           #แก้ไขข้อมูลใหม่ตามที่ส่งมาจากแบบฟอร์ม
        form.numberleave = request.POST["numberleave"]           #แก้ไขข้อมูลใหม่ตามที่ส่งมาจากแบบฟอร์ม
        form.From_Date = request.POST["From_Date"]
        form.To_Date = request.POST["To_Date"]
        form.reason = request.POST["reason"]
        
        date_format = "%d %b %Y"
        form.From_Date = datetime.strptime(form.From_Date, date_format).strftime("%Y-%m-%d")
        form.To_Date = datetime.strptime(form.To_Date, date_format).strftime("%Y-%m-%d")
        username_id = request.user.id           #ข้อมูลของผู้login

        existing_form = Form.objects.filter(
            Q(username_id=username_id) & ~Q(pk=person_id),
            From_Date__lte=form.To_Date,  # ตรวจสอบวันที่เริ่มต้นก่อนหรือเท่ากับวันที่สิ้นสุด
            To_Date__gte=form.From_Date  # ตรวจสอบวันที่สิ้นสุดหลังหรือเท่ากับวันที่เริ่มต้น
        ).first()

        if existing_form:
            # ฟอร์มการลาซ้ำกับวันที่มีอยู่ในช่วงเวลาที่กำหนด
            messages.success(request, "ฟอร์มการลาซ้ำกับวันที่มีอยู่ในช่วงเวลาที่กำหนด")
            return redirect('/formleave')
        
        
        #check have day leave
        number_instance = Number.objects.filter(username_id=username_id).first()
        
        if form.typeleave =='S' :
            type = 'ลาป่วย'
            form_instance = Form.objects.filter(username_id=username_id,show=0,typeleave='S').aggregate(total_sum=Sum('numberleave'))
            form_sum = form_instance['total_sum'] if form_instance['total_sum'] is not None else 0
            remain = number_instance.sick - form_sum
            leave_remain = number_instance.sick
            if remain < int(form.numberleave) :
               messages.success(request,"วันลาป่วยของคุณไม่เพียงพอ กรุณากรอกฟอร์มขอลาใหม่อีกครั้ง")
               return redirect('/formleave')        
            
        elif form.typeleave =='P' :
            type = 'ลากิจ'
            form_instance = Form.objects.filter(username_id=username_id,show=0,typeleave='P').aggregate(total_sum=Sum('numberleave'))
            form_sum = form_instance['total_sum'] if form_instance['total_sum'] is not None else 0
            remain = number_instance.personal - form_sum
            leave_remain = number_instance.personal
            if remain < int(form.numberleave) :
               messages.success(request,"วันลากิจของคุณไม่เพียงพอ กรุณากรอกฟอร์มขอลาใหม่อีกครั้ง")
               return redirect('/formleave')      
           
        else :
            type = 'ลาพักร้อน'
            form_instance = Form.objects.filter(username_id=username_id,show=0,typeleave='V').aggregate(total_sum=Sum('numberleave'))
            form_sum = form_instance['total_sum'] if form_instance['total_sum'] is not None else 0
            remain = number_instance.vacation - form_sum
            leave_remain = number_instance.vacation
            if remain < int(form.numberleave) :
               messages.success(request,"วันลาพักร้อนของคุณไม่เพียงพอ กรุณากรอกฟอร์มขอลาใหม่อีกครั้ง")
               return redirect('/formleave')  
    
        form.save()

        leader = request.user.leader
        person_instance = Person.objects.filter(username=leader).first()
        leader_email = person_instance.email
        leader_frist = person_instance.first_name
        leader_last = person_instance.last_name
        
        formatted_From = datetime.strptime(form.From_Date, "%Y-%m-%d").strftime(date_format)
        formatted_To = datetime.strptime(form.To_Date, "%Y-%m-%d").strftime(date_format)

        username = request.user.username
        person = Person.objects.filter(username=username)        
        html = render_to_string('emails/contactform.html',{
            'leader_frist':leader_frist,
            'leader_last':leader_last,
            'person':person,
            'type':type,
            'numberleave':form.numberleave,
            'From_Date':formatted_From,
            'To_Date':formatted_To,
            'reason':form.reason,
            'leave_remain':leave_remain
        })
        
        send_mail('เรื่อง ขออนุญาติลา (แก้ไขวันลา)','Hello', 'patinya590@gmail.com' , [leader_email],html_message=html)
        return redirect('/status')            
    else :
    #ถ้าไม่มีการส่งข้อมูลมาใช้ข้อมูลเดิม
        form = Form.objects.get(pk=person_id)
        return render(request,"edit.html",{"form":form})

@login_required( login_url='/')
def delete(request,person_id) :
    form = Form.objects.get(pk=person_id)    
    form.delete()
    messages.success(request,"ยกเลิกฟอร์มการลานี้เรียบร้อย")
    return redirect("/status")

@login_required( login_url='/')
def status(request) :
    # if request.method == "POST" :
    username_id = request.user.id 
    all_person = Form.objects.filter(username_id=username_id) 
    all_number = Number.objects.filter(username_id=username_id)
    
    return render(request,"status.html",{"all_person":all_person , "all_number":all_number})

@login_required( login_url='/')
def approve(request) :
    username = request.user.username
    allow = Form.objects.filter(username__leader=username,show=0)
    return render(request,"approve.html",{"allow":allow})


def success(request,person_id):
    
    leader_frist = request.user.first_name
    leader_last = request.user.last_name
    
    # เรียกใช้ข้อมูลจากโมเดล Form
    form_instance = Form.objects.get(pk=person_id)
    numberleave_value = form_instance.numberleave
    typeleave_value = form_instance.typeleave
    From_Date=form_instance.From_Date
    To_Date=form_instance.To_Date
    reason=form_instance.reason
    form_instance.show = 1  #เปลี่ยนเป็นTrue
    form_instance.save() 

    # เรียกใช้ข้อมูลจากโมเดล Number
    number_instance = Number.objects.filter(username=form_instance.username).first()
    
    if typeleave_value =='S' :
        type = 'ลาป่วย'
        number_instance.sick -= numberleave_value   
        leave_remain = number_instance.sick
    elif typeleave_value =='P' :
        type = 'ลากิจ'
        number_instance.personal -= numberleave_value
        leave_remain = number_instance.personal

    else :
        type = 'ลาพักร้อน'
        number_instance.vacation -= numberleave_value
        leave_remain = number_instance.vacation

        
    number_instance.save()       
    
    # เรียกใช้ข้อมูลจากโมเดล Person
    person_instance = Person.objects.filter(username=form_instance.username).first()
    person_email = person_instance.email
    
    statas = 'อนุมัติ'
          
    html = render_to_string('emails/statusform.html',{
        'leader_frist':leader_frist,
        'leader_last':leader_last,
        'first_name':person_instance.first_name,
        'last_name':person_instance.last_name,
        'position':person_instance.position,
        'team':person_instance.team,
        'level':person_instance.level,
        'type':type,
        'numberleave':numberleave_value,
        'From_Date':From_Date.strftime("%d %b %Y"),
        'To_Date':To_Date.strftime("%d %b %Y"),
        'reason':reason,
        'leave_remain':leave_remain,
        'statas':statas
    })
    
    send_mail('เรื่อง แจ้งผลอนุมัติการลา ','Hello', 'patinya590@gmail.com' , [person_email],html_message=html)
    return redirect('/approve')  


def unsuccess(request,person_id) :
    leader_frist = request.user.first_name
    leader_last = request.user.last_name
    
    form_instance = Form.objects.get(pk=person_id)
    numberleave_value = form_instance.numberleave
    typeleave_value = form_instance.typeleave
    From_Date=form_instance.From_Date
    To_Date=form_instance.To_Date
    reason=form_instance.reason
    
    form_instance.show = 1  #เปลี่ยนเป็นTrue
    form_instance.save() 
        
    # เรียกใช้ข้อมูลจากโมเดล Number
    number_instance = Number.objects.filter(username=form_instance.username).first()
    
    if typeleave_value =='S' :
        type = 'ลาป่วย'
        leave_remain = number_instance.sick
    elif typeleave_value =='P' :
        type = 'ลากิจ'
        leave_remain = number_instance.personal

    else :
        type = 'ลาพักร้อน'
        leave_remain = number_instance.vacation

    # เรียกใช้ข้อมูลจากโมเดล Person
    person_instance = Person.objects.filter(username=form_instance.username).first()
    person_email = person_instance.email
    
    formatted_From = From_Date.strftime("%d %b %Y")
    formatted_To = To_Date.strftime("%d %b %Y")
    
    statas = 'ไม่อนุมัติ'
        
    html = render_to_string('emails/statusform.html',{
        'leader_frist':leader_frist,
        'leader_last':leader_last,
        'first_name':person_instance.first_name,
        'last_name':person_instance.last_name,
        'position':person_instance.position,
        'team':person_instance.team,
        'level':person_instance.level,
        'type':type,
        'numberleave':numberleave_value,
        'From_Date':formatted_From,
        'To_Date':formatted_To,
        'reason':reason,
        'leave_remain':leave_remain,
        'statas':statas
    })
    
    send_mail('เรื่อง แจ้งผลอนุมัติการลา ','Hello', 'patinya590@gmail.com' , [person_email],html_message=html)
    return redirect('/approve')  

def logout(request):
    auth.logout(request)
    return redirect('/')