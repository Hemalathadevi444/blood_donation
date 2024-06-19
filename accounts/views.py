from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.mail import send_mail

# Create your views here.
def home(request):
	return render(request,'accounts/index.html')
def Login(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect("/user_home")
		else:
			messages.success(request,('Error Logging In - Please Try Again'))
			return redirect("/login")
	else:		
		return render(request, "accounts/login.html")
def Logout(request):
	logout(request)
	messages.success(request, "Logged Out Successfully!!")
	return render(request,'accounts/index.html')
def register(request):
	if request.method=="POST":   
		username = request.POST['username']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		phone = request.POST['phone']
		city = request.POST['city']
		blood_group = request.POST['blood_group']
		password = request.POST['password']
		confirm_password = request.POST['confirm_password']

		if password != confirm_password:
			messages.error(request, "Passwords do not match.")
			return redirect('/register')

		user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
		donors = Donor.objects.create(donor=user, phone=phone,  city=city, blood_group=blood_group)
		user.save()
		donors.save()
		return render(request, "accounts/index.html")
	return render(request, "accounts/register.html")
def user_base(request):
	return render(request,'accounts/user_base.html')
def user_home(request):
	return render(request,'accounts/user_home.html')
def request_page(request):
	return render(request,'accounts/request_page.html')

@login_required(login_url = '/login')
def view_profile(request):
    donor_profile = Donor.objects.get(donor=request.user)
    return render(request, "accounts/view_profile.html", {'donor_profile':donor_profile})
@login_required(login_url='/login')
def make_request(request):
	if request.method == "POST":
		name = request.POST['name']
		email = request.POST['email']
		phone = request.POST['phone']
		city = request.POST['city']
		blood_group = request.POST['blood_group']
		user=request.user
		blood_requests = RequestBlood.objects.create(name=name, email=email, phone=phone, city=city,blood_group=blood_group,user=user)
		blood_requests.save()
		donors=Donor.objects.filter(city=city,blood_group=blood_group)
		for i in donors:
			user1=User.objects.get(id=i.donor_id)
			mail=user1.email
			send_mail("Blood request","You have a request for blood donation.Please check your profile \n Thank you!","lifesavior03@gmail.com",[mail],fail_silently=False)
		
		return render(request, "accounts/user_home.html")
	return render(request, "accounts/make_request.html")

@login_required(login_url='/login')
def requests(request):
	donor=Donor.objects.get(donor=request.user)
	requests=RequestBlood.objects.all().filter(city=donor.city,blood_group=donor.blood_group)
	return render(request,'accounts/requests.html',{'requests':requests,'donor':donor})

@login_required(login_url='/login')
def accepted_requests(request):
	requests=RequestBlood.objects.filter(user_id=request.user.id)
	if requests:
		for i in requests:
			accepted_requests=AcceptedDonors.objects.all().filter(city=i.city,blood_group=i.blood_group)
		return render(request,'accounts/accepted_requests.html',{'requests':requests,'accepted_requests':accepted_requests})
	else:
		return render(request,'accounts/accepted_requests.html',{'requests':requests})
@login_required(login_url = '/login')
def edit_profile(request):
    donor_profile = Donor.objects.get(donor=request.user)
    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['phone']
        city = request.POST['city']

        donor_profile.donor.email = email
        donor_profile.phone = phone
        donor_profile.city = city
        donor_profile.save()
        donor_profile.donor.save()
        return render(request, "accounts/user_home.html")
    return render(request, "accounts/edit_profile.html", {'donor_profile':donor_profile})

@login_required(login_url = '/login')
def delete(request):
	requests=RequestBlood.objects.filter(user_id=request.user.id)
	for i in requests:
		accepted_requests=AcceptedDonors.objects.all().filter(city=i.city,blood_group=i.blood_group)
	requests.delete()
	accepted_requests.delete()
	return redirect('/request_page')

@login_required(login_url = '/login')
def accept(request):
	donor=Donor.objects.get(donor=request.user)
	name=request.user.first_name
	phone=donor.phone
	city=donor.city
	blood_group=donor.blood_group
	accepted_donors=AcceptedDonors.objects.create(name=name,phone=phone,city=city,blood_group=blood_group)
	return redirect('/requests')



