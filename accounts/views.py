from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import CreateUserForm, CustomerForm, leaveform
from .filters import EmpFilter, AttenFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.utils import timezone
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from crm1 import settings
from pytz import timezone
from datetime import datetime, date, timedelta
from django.http import HttpResponse
from django.contrib import messages
import os

#@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')


			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
# @admin_only
def home(request):

	if request.method == 'POST':
		if 'btnform1' in request.POST:
			if datetime.now(timezone("Asia/Kolkata")).time().strftime("%H:%M:%p") >= "06:00:pm":
				user_list = list(User.objects.all().values_list('username', flat=True))
				atten_list = list(Attendance.objects.filter(date = datetime.now()).values_list('attender', flat=True))
				absent_list = [absent for absent in user_list if absent not in atten_list]
				print(absent_list)
				for emp in absent_list:
					put_absent = Attendance.objects.create(attender = emp, date = datetime.now(), is_present = False)
					put_absent.save()

		# date_filter = request.POST['date']
		# print(date_filter)

	customers = Customer.objects.all()
	user = User.objects.all()
	attend = Attendance.objects.all().order_by('date').reverse()
	employees = user.exclude(is_staff=True).count()
	managers = user.filter(is_staff=True).count()
	total_stackholders = user.count()
	present = attend.filter(is_present=True)

	# f = EmpFilter(request.GET, queryset=Customer.objects.all()) 'atten_filter' : atten_filter, 'atten_has_filter' : atten_has_filter
	# has_filter = any(field in request.GET for field in set(f.get_fields()))
	
	f = AttenFilter(request.GET, queryset=Attendance.objects.all().order_by('date').reverse())
	has_filter = any(field in request.GET for field in set(f.get_fields()))

	context = {'customers':customers, 'user':user,
	'employees':employees,'managers':managers,
	'total_stackholders':total_stackholders, 'filter': f, 'has_filter': has_filter,
	'present' : present, 
	}

	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['customer', 'admin'])
def accountSettings(request):
	customer = User.objects.get(pk=request.user.id).customer #request.user.customer #Customer.objects.get(name=request.user)
	print('customer name: ', customer)
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def detail_view(request, pk):
	name = Customer.objects.get(id=pk)
	employee = Attendance.objects.filter(attender=name)
	f = AttenFilter(request.GET, queryset=Attendance.objects.filter(attender=name))
	has_filter = any(field in request.GET for field in set(f.get_fields()))

	context = {'employee':employee, 'filter': f, 'has_filter': has_filter, 'name' : name}
	return render(request, 'accounts/detail_view.html', context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def delete_emp(request, pk):
	employee = Customer.objects.get(id=pk)
	user = User.objects.get(username=employee)
	atten = Attendance.objects.filter(attender=employee)
	if request.method == "POST":
		employee.delete()
		user.delete()
		atten.delete()
		return redirect('home')

	context = {'item':employee}
	return render(request, 'accounts/delete.html', context)

# clockin & clockout

@login_required(login_url='login')
# @allowed_users(allowed_roles=['customer', 'admin'])
def clockin_clockout(request):
	if request.method == 'POST':
		if 'btnform1' in request.POST:
			if Attendance.objects.filter(attender=str(request.user), date = datetime.utcnow(), is_present = False).exists():
				messages.error(request, "You are marked as absent by admin today, you can't clock-in")
			elif not Attendance.objects.filter(attender=str(request.user),date = datetime.utcnow(), clockin__isnull=False).exists():
				clockin_model = Attendance.objects.create(attender = str(request.user), date = datetime.now(), clockin = datetime.now(), is_present = True)
				clockin_model.save()
				messages.success(request, 'You have Clocked In today')
			else:
				messages.info(request, 'You can Clock In once a day')

		elif 'btnform2' in request.POST:
			if not Attendance.objects.filter(attender=str(request.user),date = datetime.utcnow(), clockin__isnull=False).exists():
				messages.error(request, 'You must clockin to clockout')
			elif not Attendance.objects.filter(attender=str(request.user),date = datetime.utcnow(), clockout__isnull=False).exists():
				clockout_model = Attendance.objects.select_related().filter(attender = str(request.user), date = date.today()).update(clockout = datetime.now())
				messages.success(request, 'You have Clocked out today')
			else:
				messages.info(request, 'You can Clock out once a day')
	today = date.today()
	seven_day_before = today - timedelta(days=7)
	context = {'show_table' : Attendance.objects.filter(attender=str(request.user), date__gte=seven_day_before)}
	return render(request, 'accounts/attendance.html', context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['customer', 'admin'])
def DownloadPdf(request):
    with open(os.path.join(settings.MEDIA_ROOT, 'Leave Management policies.pdf'), 'rb') as fh:
    	response = HttpResponse(fh.read(), content_type="application/pdf")
    	response['Content-Disposition'] = 'inline; filename=invoice.pdf'
    	return response


@login_required(login_url='login')
# @allowed_users(allowed_roles=['customer', 'admin'])
def leave_application(request):
	
	form = leaveform(request.POST)
	if request.method == 'POST' and form.is_valid():	
		print(settings.EMAIL_HOST_USER)
		# if form.is_valid():
		print(User.email)
		from_email = settings.EMAIL_HOST_USER
		to_email = form.cleaned_data['to_email']
		print(to_email)
		subject = form.cleaned_data['subject']
		message = form.cleaned_data['content']
		cc = form.cleaned_data['cc']

		email = EmailMessage(subject, message, from_email, [to_email], [cc], headers = {'Reply-To': from_email})

		email.send()
		messages.success(request, 'Mail Sent successfully')
		return HttpResponse("Mail Sent Successfully")
	else:
		form = leaveform(user=request.user) # Clear the form
	return render(request, 'accounts/leave_application.html', {"form": form})


	