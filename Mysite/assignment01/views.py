import imp
from django.shortcuts import render,redirect
from matplotlib import widgets
from assignment01 import models
from django import forms, http
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404, FileResponse
import smtplib
import ssl
import assignment01.utils.mysql_excel as export
from email.message import EmailMessage
class email:
    def __init__(self,EMAIL_ADDRESS,EMAIL_PASSWORD,receiver,subject,body):
        self.EMAIL_ADDRESS = EMAIL_ADDRESS
        self.EMAIL_PASSWORD = EMAIL_PASSWORD
        self.receiver = receiver
        self.subject = subject
        self.body = body
    def sendemail(self):
        msg = EmailMessage()
        msg['subject'] = self.subject
        msg['From'] = self.EMAIL_ADDRESS
        msg['To'] = self.receiver 
        msg.set_content(self.body)
        with smtplib.SMTP_SSL('smtp.126.com',465) as smtp:
            smtp.login(self.EMAIL_ADDRESS,self.EMAIL_PASSWORD)
            # msg = f"Subject:{self.subject}\n\n{self.body}"
            smtp.send_message(msg)

class LoginModelForm(forms.ModelForm):
    class Meta:
        model = models.admin
        fields = ["username","password"]
        widgets = {
              'username':forms.TextInput(attrs={"class":"form-control","placeholder":"用户名"}),
              'password':forms.TextInput(attrs={"class":"form-control","placeholder":"密码",'type':'password'}),
        }
    """ def clean_password(self):
        user = self.data.get('username')
        pwd = self.cleaned_data['password']
        datalist = models.admin.objects.filter(username = user).first()
        exists = models.admin.objects.filter(username = user).exists()
        if not exists:
            raise ValidationError('username not exists')
        elif datalist.password != pwd:
            raise ValidationError('password not correct')
        return pwd """
class ListModelForm(forms.ModelForm):
    class Meta:
        model = models.equipment_info
        fields = ['number','name','specification','price','date','Manufacturer','buyer','state']
        widgets = {
              'date':forms.TextInput(attrs={"class":"form-control","placeholder":"日期",'type':'date'}),
        }
    def __init__(self ,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class':'form-control','placeholder':field.label}
                
class UpdateModelForm(forms.ModelForm):
    class Meta:
        model = models.equipment_info
        fields = ['number','name','specification','price','date','Manufacturer','buyer','state']
        widgets = {
              'date':forms.TextInput(attrs={"class":"form-control","placeholder":"日期",'type':'date'}),
        }
    def __init__(self ,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class':'form-control','placeholder':field.label}

    def clean_number(self):
        number1 = self.cleaned_data['number']
        exists = models.equipment_info.objects.exclude(id = self.instance.pk).filter(number = number1).exists()
        if exists:
            raise ValidationError('编号已存在')
        return number1

class BrokenModelForm(forms.ModelForm):
    class Meta:
        model = models.equipment_info
        fields = ['number','name','specification','price','date','Manufacturer','buyer','state']
        widgets = {
              'date':forms.TextInput(attrs={"class":"form-control","placeholder":"日期",'type':'date'}),
        }
    def __init__(self ,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class':'form-control','placeholder':field.label}

class ReportModelForm(forms.ModelForm):
    class Meta:
        model = models.Toberepaired
        fields = ['number','price','date','manufacturer','responsible']
        widgets = {
              'date':forms.TextInput(attrs={"class":"form-control","placeholder":"日期",'type':'date'}),
        }
    def __init__(self ,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class':'form-control','placeholder':field.label}
        
def report(request):
    if request.method == 'GET':
        form = ReportModelForm()
        return render(request,'report.html',{'form':form})
    form = ReportModelForm(data=request.POST)
    if form.is_valid():
        number1 = form.cleaned_data['number']
        exists = models.equipment_info.objects.filter(number = number1).exists()
        if not exists:
            form.add_error('number','编号不存在')
            return render(request,'report.html',{'form':form})
        form.save()
        return redirect('/broken/')
    return render(request,'report.html',{'form':form})


def login(request):
    if request.method == 'GET':
        form = LoginModelForm()
        return render(request,'login.html',{'form':form})
    form = LoginModelForm(data=request.POST)
    if form.is_valid(): 
        user = form.cleaned_data['username']
        pwd = form.cleaned_data['password']
        datalist = models.admin.objects.filter(username = user).first()
        exists = models.admin.objects.filter(username = user).exists()
        if not exists:
            form.add_error('username','username not exists')
            return render(request,'login.html',{'form':form})
        elif datalist.password != pwd:
            form.add_error('password','password not correct')
            return render(request,'login.html',{'form':form}) 
        request.session['info'] = {'name':user}
        return redirect('/list/')
    return render(request,'login.html',{'form':form})
""" def register(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request,'register.html',{'form':form})
    form = RegisterModelForm(data=request.POST)
    if form.is_valid(): 
        form.save()
        return redirect('/login/')
    return render(request,'register.html',{'form':form})
 """
def list(request):
    form = models.equipment_info.objects.filter(state ='1').order_by('number')
    return render(request,'list.html',{'form':form})

def logout(request):
    request.session.clear()
    return redirect('/login/')

def add(request):
    if request.method == 'GET':
        form = ListModelForm()
        return render(request,'add.html',{'form':form})
    form = ListModelForm(data=request.POST)
    if form.is_valid():
        number1 = form.cleaned_data['number']
        exists = models.equipment_info.objects.filter(number = number1).exists()
        if exists:
            form.add_error('number','编号已存在')
            return render(request,'add.html',{'form':form})
        form.save()
        if form.cleaned_data['state'] != 1 :
            return redirect('/broken/')
        return redirect('/list/')
    return render(request,'add.html',{'form':form})


def update(request,nid):
    row_obj = models.equipment_info.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = UpdateModelForm(instance = row_obj)
        return render(request,'update.html',{'form':form})
    form =UpdateModelForm(data=request.POST,instance = row_obj)
    if form.is_valid():
        form.save()
        if form.cleaned_data['state'] !='1':
            return redirect('broken')
        return redirect('/list/')
    return render(request,'update.html',{'form':form})
    
def delete(request,nid,nnumber):
    models.equipment_info.objects.filter(id = nid).delete()
    models.Toberepaired.objects.filter(number = nnumber).delete()
    print(nnumber)
    return redirect('/list/')

def broken(request):
    form = models.equipment_info.objects.exclude(state = '1').all().order_by('number')
    form2 = models.Toberepaired.objects.all().order_by('number')
    return render(request,'broken.html',{'form':form,'form2':form2})

def deletereport(request,nid):
    models.Toberepaired.objects.filter(id = nid).delete()
    return redirect('/broken/')
def application(request,nid):
    if request.method == 'GET':
        row_object = models.equipment_info.objects.filter(id=nid).first()
        return render(request,'application.html',{'row_object':row_object})
    sender = request.POST.get('sender') 
    password = request.POST.get('password') 
    receiver = request.POST.get('receiver') 
    subject = request.POST.get('subject') 
    body = subject = request.POST.get('body')
    form  = email(sender,password,receiver,subject,body)
    form.sendemail()
    return redirect('/list/')

def file_download(request):
    export.export()
    file = open(r'C:\Users\惠普\Desktop\Mysite\assignment01\static\data.xlsx', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    # 设置下载名
    response['Content-Disposition'] = "attachment;filename=data.xlsx"
    return response

