"""bot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import url
from django.contrib import admin

from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from chatting import views

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^', include(router.urls)),
    url(r'^result$', 'chatting.views.result'),
    url(r'^emo$', 'emotion.views.find_emotion'),
    url(r'^chats$', 'chatting.views.chats'),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^home$', 'bot.views.home'),

    # user auth urls
    url(r'^accounts/login/$', 'bot.views.login'),
    url(r'^accounts/auth/$', 'bot.views.auth_view'),
    url(r'^accounts/logout/$', 'bot.views.logout'),
    url(r'^accounts/loggedin/$', 'bot.views.loggedin'),
    url(r'^accounts/invalid_login/$', 'bot.views.invalid_login'),

    # user registration
    url(r'^accounts/register/$', 'bot.views.register_user'),
    url(r'^accounts/register_success/$', 'bot.views.register_success'),
    
    # user profile
    url(r'^profile/emotions$', 'user_profile.views.get_emotions_score'),
    

    url(r'^$', 'bot.views.chatting'),
]
