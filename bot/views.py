from django.shortcuts import render_to_response
from django.http 				import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from forms import MyRegistrationForm
from django.conf import settings

from chatting.models import Session
from django.contrib.auth.models import User
from user_profile.models import UserProfile

# from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.mail import send_mail
import logging
logr = logging.getLogger(__name__)

def login(request):
	if(request.user.is_authenticated()):
		return HttpResponseRedirect(settings.BASE_URL+'/accounts/loggedin/')
	c = {
		'BASE_URL': settings.BASE_URL	
	}
	c.update(csrf(request))
	return render_to_response('login.html',c)

def auth_view(request):
	username = request.POST.get('username','')
	password = request.POST.get('password','')
	user = auth.authenticate(username=username, password=password)

	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect(settings.BASE_URL)
	else:
		return HttpResponseRedirect(settings.BASE_URL+'/accounts/invalid_login/')

def loggedin(request):
	if(not request.user.is_authenticated()):
		return HttpResponseRedirect(settings.BASE_URL+'/accounts/login/')
	return render_to_response('loggedin.html',
							 {'full_name':request.user.username,'BASE_URL': settings.BASE_URL})

def invalid_login(request):
	return render_to_response('invalid_login.html',{
		'BASE_URL': settings.BASE_URL	
		})

def logout(request):
	auth.logout(request)
	return render_to_response('logout.html',{
		'BASE_URL': settings.BASE_URL	
		})

def register_user(request):
	if request.method == 'POST':
		form = MyRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			# up = UserProfile(user=form.u, joy_count=1, dis_count=1, ang_count=1, fea_count = 1, sad_count=1)
			# up.save()
			# return render_to_response('register')
			return HttpResponseRedirect(settings.BASE_URL+'/accounts/register_success')

	args = {}
	args.update(csrf(request))
	args['form'] = MyRegistrationForm()
	args['BASE_URL'] = settings.BASE_URL
	return render_to_response('register.html', args)

def register_success(request):
	# u = User.objects.get(id = request.user.id)
	# up = UserProfile(user=u, joy_count=1, dis_count=1, ang_count=1, fea_count = 1, sad_count=1)
	# up.save()

	return render_to_response('register_success.html',{
		'BASE_URL': settings.BASE_URL	
		})

def chatting(request):
	if(request.user.is_authenticated()):
		user = request.user

		if request.method == 'GET':
			sess = request.GET.get('sess')
			if(sess == "new"):
				# new
				s = Session(name="new session", user_id=user)
				s.save()
				return HttpResponseRedirect(settings.BASE_URL+'/?sess=' + str(s.id))
			else:
				# find if exist
				try:
				    s = Session.objects.get(id=sess)
				except Session.DoesNotExist:
				    s = None
				
				if(s is None):
					return HttpResponseRedirect(settings.BASE_URL+'/home')

		html =  render_to_response('chatting.html',{
		'BASE_URL': settings.BASE_URL,
		'RNN_URL': settings.RNN_URL,
		'session_id': s.id 		
		})
		return HttpResponse(html)
	return HttpResponseRedirect(settings.BASE_URL+'/accounts/login/')





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
	return HttpResponseRedirect(settings.BASE_URL+'/accounts/login/')