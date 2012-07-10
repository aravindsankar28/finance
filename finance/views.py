
from django.http import *
from django.shortcuts import *
from django.template import *
from django.contrib import auth
from users.models import UserProfile
from django.contrib.auth.models import *
from home.models import *
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
	
def corepage(request,foobar):
	if request.user.is_authenticated():
		return render_to_response('CorePage.html',locals(),context_instance=RequestContext(request))
	return HttpResponseRedirect('/login/')
	
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")
  
def budget(request,foobar):		
	us = User.objects.get(pk = foobar)
	
	
	if us.get_profile().is_finance_core():
		try:
			b = Budget.objects.filter(approve = False)
		except Budget.DoesNotExist:
			b = None		
		size  = len(b)			
		spA = []
		spB =[]
		#sp = [] 
		for budget in b :		
			tempA = SplitA.objects.filter(budgetid = budget.budgetid) 
			spA.append(tempA)
			tempB = SplitB.objects.filter(budgetid = budget.budgetid) 
			spB.append(tempB)
			#return HttpResponse(temp[0].budgetid)
		return render_to_response('Budget.html',locals(),context_instance=RequestContext(request))
		
	try:
		u = UserEvent.objects.filter(user = us)
	except User.DoesNotExist:
		u  = None
	try:
		b = Budget.objects.get(user = us)
		sp1 = SplitA.objects.filter(budgetid = b.budgetid)
		sp2 = SplitB.objects.filter(budgetid = b.budgetid)
	except Budget.DoesNotExist:
		b = None
	#sp1 = SplitA.objects.filter(budgetid = b.budgetid)
	if request.method == "POST" :
		PlanA = request.POST['PlanA']
		PlanB = request.POST['PlanB']
		splitA1 = request.POST.getlist('rowA1')
		splitA2 = request.POST.getlist('rowA2')	
		splitB1 = request.POST.getlist('rowB1')
		splitB2 = request.POST.getlist('rowB2')	
		#return HttpResponse(splitA1[1]+' '+ splitA2[1]) 
		#splitA2 = request.POST['row2'].getlist()
		#splitB = request.POST['splitB']
		if b is None:	
			b = Budget(user = us)			
			b.planA = PlanA
			b.planB = PlanB
			b.save()
			for s,t in zip(splitA1,splitA2):	
				if b.budgetid is not None:
					sp = SplitA(budgetid = b.budgetid)
				sp.item = s
				sp.price = t
				sp.save()
			for u,v in zip(splitB1,splitB2):	
				if b.budgetid is not None:
					sp = SplitB(budgetid = b.budgetid)
				sp.item = u
				sp.price = v
				sp.save()
		
		#b.splitA  = splitA
		#b.splitB = splitB		
				b.save()
		#sa  = splitA(budget = b)
		#sb  = splitB(budget = b)
		
		return HttpResponseRedirect('/corepage/'+foobar+'/')
	if b is not None and b.approve == False:
		return HttpResponse("Pending approval")
	return render_to_response('Budget.html',locals(),context_instance=RequestContext(request))
	
def approve(request,foobar):
	b = Budget.objects.get(budgetid = foobar)
	b.approve = True
	b.save()
	return HttpResponseRedirect('/budget/'+str(request.user.get_profile().userid)+'/')

def reject(request,foobar):
	b = Budget.objects.get(budgetid = foobar)
	b.delete()	
	return HttpResponseRedirect('/budget/'+str(request.user.get_profile().userid)+'/')	
	