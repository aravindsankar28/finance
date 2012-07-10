from django.http import *
from django.shortcuts import *
from django.template import *
from django.contrib import auth
def login(request):
	return render_to_response('LoginPage.html',locals(),context_instance=RequestContext(request))
