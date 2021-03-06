from django.shortcuts import *
from django.template import *
from django.contrib.auth import models
from django.contrib.auth.models import *
from home.models import *
def createUser(request):
	if not request.user.is_authenticated():
		return HttpResponse("Not authorised")
	#if not request.user.is_superuser:
	#	return HttpResponse("Not authorised")
	event = events.objects.all()
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		name = request.POST['option']
		u = User(username = username)
		u.set_password(password)
		u.save()
		if name == 'EventCore':
			g = Group.objects.get(name = 'EventCore')
			g.user_set.add(u)
			g.save()
		elif name == 'EventCoord':
			event = request.POST['event']
			ue = UserEvent(user = u )
			e = events.objects.get(name = event)
			ue.event = e
			ue.save()
			g = Group.objects.get(name = 'EventCoord')
			g.user_set.add(u)
			g.save()
		
		elif name == 'FinanceCore':
			g = Group.objects.get(name = 'FinanceCore')
			g.user_set.add(u)
			g.save()
		
		elif name == 'FinanceCoord':
			event = request.POST['event']
			ue = UserEvent(user = u )
			e = events.objects.get(name = event)
			ue.event = e
			ue.save()
			g = Group.objects.get(name = 'FinanceCoord')
			g.user_set.add(u)
			g.save()
		
		u.save()	
		return HttpResponseRedirect('/')
	return render_to_response('CreateUser.html',locals(),context_instance=RequestContext(request))
def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request,user)
			a =  user.get_profile()
			return HttpResponseRedirect('/corepage/'+str(a.userid)+'/')
		return render_to_response('LoginPage.html',locals(),context_instance=RequestContext(request))
	return render_to_response('LoginPage.html',locals(),context_instance=RequestContext(request))
	
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")
def editprofile(request):
	u = request.user
	us = u.get_profile()
	if request.method =='POST':
		u.first_name=request.POST['first_name']
		u.last_name=request.POST['last_name']
		u.username=request.POST['username']
		u.email=request.POST['email']
		u.save()
		return HttpResponseRedirect('/corepage/'+str(us.userid))
	return render_to_response('EditProfile.html',locals(),context_instance=RequestContext(request))
def changepw(request):
	u = request.user
	us = u.get_profile()
	if request.method =='POST':
		oldpw = request.POST['oldpw']
		newpw = request.POST['newpw']
		confirm = request.POST['confirmpw']
		if u.check_password(oldpw) == True :
			u.set_password(newpw)
			u.save()
			return HttpResponseRedirect('/corepage/'+str(us.userid))
		return render_to_response('ChangePw.html',locals(),context_instance=RequestContext(request))
	return render_to_response('ChangePw.html',locals(),context_instance=RequestContext(request))