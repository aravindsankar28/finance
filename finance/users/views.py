from django.shortcuts import *
from django.template import *
from django.contrib.auth import models
from django.contrib.auth.models import *
def createUser(request):
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
			g = Group.objects.get(name = 'EventCoord')
			g.user_set.add(u)
			g.save()
		
		elif name == 'FinanceCore':
			g = Group.objects.get(name = 'FinanceCore')
			g.user_set.add(u)
			g.save()
		
		elif name == 'FinanceCoord':
			g = Group.objects.get(name = 'FinanceCoord')
			g.user_set.add(u)
			g.save()
		
		u.save()	
		return HttpResponseRedirect('/corepage/'+str(u.get_profile().userid)+'/')
	return render_to_response('CreateUser.html',locals(),context_instance=RequestContext(request))