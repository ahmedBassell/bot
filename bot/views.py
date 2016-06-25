from django.shortcuts import render_to_response
from django.http 				import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from forms import MyRegistrationForm
from django.conf import settings

from chatting.models import Session

# from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.mail import send_mail
import logging
logr = logging.getLogger(__name__)

def login(request):
	if(request.user.is_authenticated()):
		return HttpResponseRedirect('/accounts/loggedin/')
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html',c)

def auth_view(request):
	username = request.POST.get('username','')
	password = request.POST.get('password','')
	user = auth.authenticate(username=username, password=password)

	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/accounts/invalid_login/')

def loggedin(request):
	if(not request.user.is_authenticated()):
		return HttpResponseRedirect('/accounts/login/')
	return render_to_response('loggedin.html',
							 {'full_name':request.user.username})

def invalid_login(request):
	return render_to_response('invalid_login.html')

def logout(request):
	auth.logout(request)
	return render_to_response('logout.html')

def register_user(request):
	if request.method == 'POST':
		form = MyRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/accounts/register_success')

	args = {}
	args.update(csrf(request))
	args['form'] = MyRegistrationForm()
	return render_to_response('register.html', args)

def register_success(request):
	return render_to_response('register_success.html')

def chatting(request):
	if(request.user.is_authenticated()):
		user = request.user

		if request.method == 'GET':
			sess = request.GET.get('sess')
			if(sess == "new"):
				# new
				s = Session(name="new session", user_id=user)
				s.save()
				return HttpResponseRedirect('/?sess=' + str(s.id))
			else:
				# find if exist
				try:
				    s = Session.objects.get(id=sess)
				except Session.DoesNotExist:
				    s = None
				
				if(s is None):
					return HttpResponseRedirect('/home')

		html =  render_to_response('chatting.html',{
		'BASE_URL': settings.BASE_URL,
		'session_id': s.id 		
		})
		return HttpResponse(html)
	return HttpResponseRedirect('/accounts/login/')





# start new session
# or get some session
def home(request):
	if(request.user.is_authenticated()):
		user = request.user
		try:
			sessions = Session.objects.filter(user_id = request.user)
		except Session.DoesNotExist:
			sessions = None
		html =  render_to_response('home.html',{
		'BASE_URL': settings.BASE_URL,
		'user' : user,
		'sessions': sessions
		})
		return HttpResponse(html)
	return HttpResponseRedirect('/accounts/login/')