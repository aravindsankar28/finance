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
		if int(foobar) == request.user.get_profile().userid:
			try:
				ue = UserEvent.objects.get(user = request.user)		
			except UserEvent.DoesNotExist:
				ue = None
				return render_to_response('CorePage.html',locals(),context_instance=RequestContext(request))
			return render_to_response('CorePage.html',locals(),context_instance=RequestContext(request))
		return HttpResponse("You are not authorised to view this page ")
	return HttpResponse("You are not authorised to view this page ")
	
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")
  
def budget(request):		
	#us = User.objects.get(pk = foobar)
	if request.user.get_profile().is_event_core():
		budgets = Budget.objects.all()
		sp = []
		for b in budgets:
			tempA = SplitA.objects.filter(budgetid = b.budgetid)
			sp.append(tempA)
		#return render_to_response('Advance.html',locals(),context_instance=RequestContext(request))
		return render_to_response('Budget.html',locals(),context_instance=RequestContext(request))
	if request.user.get_profile().is_finance_core():
		try:
			b = Budget.objects.filter(approve = False)
		except Budget.DoesNotExist:
			b = None		
		size  = len(b)			
		spA = []
		spB =[]
		#sp = [] 
		#return HttpResponse(b[0].approve)
		for budget in b :		
			tempA = SplitA.objects.filter(budgetid = budget.budgetid) 
			spA.append(tempA)
			tempB = SplitB.objects.filter(budgetid = budget.budgetid) 
			spB.append(tempB)
		return render_to_response('Budget.html',locals(),context_instance=RequestContext(request))
		
	try:
		u = UserEvent.objects.get(user = request.user)
	except UserEvent.DoesNotExist:
		u  = None
	try:
		b = Budget.objects.get(event = u.event)
		sp1 = SplitA.objects.filter(budgetid = b.budgetid)
		sp2 = SplitB.objects.filter(budgetid = b.budgetid)
	except Budget.DoesNotExist:
		b = None
	#sp1 = SplitA.objects.filter(budgetid = b.budgetid)
	if request.method == "POST" :
		splitA1 = request.POST.getlist('rowA1')
		splitA2 = request.POST.getlist('rowA2')	
		splitB1 = request.POST.getlist('rowB1')
		splitB2 = request.POST.getlist('rowB2')	
		#return HttpResponse(splitA1[1]+' '+ splitA2[1]) 
		#splitA2 = request.POST['row2'].getlist()
		#splitB = request.POST['splitB']
		PlanA = 0 
		PlanB = 0 
		if b is None:	
			b = Budget(event = u.event)			
			b.save()
			for s,t in zip(splitA1,splitA2):	
				if b.budgetid is not None:
					sp = SplitA(budgetid = b.budgetid)
					
				sp.item = s
				sp.price = t
				sp.balance = t
				sp.amount_debit = 0 
				sp.status = str(sp.balance) 
				PlanA = PlanA + int(t)  
				sp.save()
			for u,v in zip(splitB1,splitB2):	
				if b.budgetid is not None:
					sp = SplitB(budgetid = b.budgetid)
					
				sp.item = u
				sp.price = v
				sp.balance = v
				sp.status = str(sp.balance) 
				PlanB = PlanB + int(v)
				sp.save()
			b.planA = PlanA
			b.planB = PlanB
			b.save()		
				
		#sa  = splitA(budget = b)
		#sb  = splitB(budget = b)
		
		return HttpResponseRedirect('/corepage/'+str(request.user.get_profile().userid)+'/')
	if b is not None and b.approve == False:
		return HttpResponse("Pending approval")
	return render_to_response('Budget.html',locals(),context_instance=RequestContext(request))
	
def approve(request,foobar):
	b = Budget.objects.get(budgetid = foobar)
	b.approve = True
	b.save()
	return HttpResponseRedirect('/budget/'+str(b.event.event_id)+'/')

def reject(request,foobar):
	b = Budget.objects.get(budgetid = foobar)
	e = b.event
	b.delete()
	spA = SplitA.objects.filter(budgetid = foobar)
	spB = SplitB.objects.filter(budgetid = foobar)
	spA.delete()
	spB.delete()
	return HttpResponseRedirect('/budget/'+str(e.event_id)+'/')	

def advance(request):
	if request.method == 'POST':
		amount = int(request.POST['amount'])
		spid = request.POST['spid']
		s = SplitA.objects.get(spid = spid)
		if amount > s.balance :
			return HttpResponseRedirect('/advanceRequirements/')
		else:
			s.balance = s.balance - int(amount)
			s.status = "Pending"
			s.amount_debit = amount
			s.save()
			b = Budget.objects.get(budgetid = s.budgetid)
			b.item_approval = True
			b.save()
			return HttpResponseRedirect('/advanceRequirements/')
	if request.user.get_profile().is_event_core():
		budgets = Budget.objects.all()
		sp = []
		for b in budgets:
			tempA = SplitA.objects.filter(budgetid = b.budgetid)
			sp.append(tempA)
		return render_to_response('Advance.html',locals(),context_instance=RequestContext(request))
	if not request.user.get_profile().is_finance_core():
		try:
			u = UserEvent.objects.get(user = request.user)
		except User.DoesNotExist:
			u  = None
		try:
			b = Budget.objects.get(event = u.event)
			#b = Budget.objects.get(pk = foobar)
			spA = SplitA.objects.filter(budgetid = b.budgetid)	
			if b.approve == False:
				return HttpResponse("Budget pending approval ")
		except Budget.DoesNotExist:
			b = None
		except SplitA.DoesNotExist:
			spA = None
		return render_to_response('Advance.html',locals(),context_instance=RequestContext(request))
	try:	
		budgets = Budget.objects.filter(item_approval = True)
	except Budget.DoesNotExist:
		budgets = None
	sp = []
	for b in budgets:
		tempA = SplitA.objects.filter(budgetid = b.budgetid)
		sp.append(tempA)
	return render_to_response('Advance.html',locals(),context_instance=RequestContext(request))
def approve_advance(request,foobar):
	s = SplitA.objects.get(spid = foobar)
	s.approve = True
	s.status = str(s.balance)
	s.amount_debit = 0 
	s.save()
	try:
		budgets = Budget.objects.filter(budgetid = s.budgetid)
	except Budget.DoesNotExist:
		budgets = None
	if budgets == None:
		b = Budget.objects.get(budgetid = s.budgetid)
		b.item_approval = False
		b.save()
	return HttpResponseRedirect('/advanceRequirements/')
	
def event(request,foobar):
	event  = events.objects.all()
	return render_to_response('Events.html',locals(),context_instance=RequestContext(request))
