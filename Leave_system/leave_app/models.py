from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.html import format_html
from django.core.validators import MinValueValidator


# Create your models here.

LEAVE_CHOICE = (
    ('S','Sick Leave'),
    ('P','Personal Leave'),
    ('V','Vacation Leave'),
)


class Person(AbstractUser):
    nickname = models.CharField(max_length=100,null=True)
    tel = models.CharField(max_length=20,null = True)
    team = models.CharField(max_length=100,null=True) 
    position = models.CharField(max_length=100,null=True) 
    leader = models.CharField(max_length=100,null=True) 
    level = models.CharField(max_length=1,null=True)   #ลาพักร้อน

    def __str__(self):
        return str(self.username)


class Number(models.Model):
    # user = models.ForeignKey(Form,on_delete=models.CASCADE,primary_key=True)
    # name = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='name_from')
    username = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        primary_key=True,
        # db_column="username"
    )
    sick = models.IntegerField(default=30 , validators=[MinValueValidator(0)])    #ลาป่วย
    personal = models.IntegerField(default=10 , validators=[MinValueValidator(0)])  #ลากิจ
    vacation = models.IntegerField(default=8 , validators=[MinValueValidator(0)])   #ลาพักร้อน
 
    def __str__(self):
        return str(self.username.username)
    

class Form(models.Model):
    # name = models.CharField(max_length=100)
    # email = models.CharField(max_length=100) 
    # user = models.OneToOneField(ชื่อตารางพนักงาน,on_delete=models.CASCADE,primary_key=True,)
    date = models.DateTimeField(auto_now = False, auto_now_add = True, null = False, blank = True)  
    username = models.ForeignKey(Person, on_delete=models.CASCADE )
    typeleave = models.CharField(max_length=5 , null=True , blank=True , choices=LEAVE_CHOICE)
    numberleave = models.IntegerField()
    From_Date = models.DateField()    
    To_Date = models.DateField()  
    reason = models.CharField(max_length=100,null = True)
    show = models.BooleanField(default=False)
    class Meta:
        get_latest_by = 'date'
    
    def __str__(self):
        return str(self.username.username)
    