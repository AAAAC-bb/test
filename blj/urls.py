"""blj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from audit import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^signin/$', views.signin),
    url(r'^exit/$', views.exit),
    
    url(r'^$', views.index, name='index'),
    url(r'^hostlist/$', views.hostlist, name='host_list'),

    url(r'^api/hostlist/$', views.api_host_list, name='api_host_list'),
    url(r'^api/token/$', views.api_host_token, name='get_token'),

]
