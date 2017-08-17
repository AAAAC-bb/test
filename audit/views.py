from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from audit import models
import datetime
import random
import string
import json


# Create your views here.
@login_required
def index(requests):
    return render(requests, 'index.html')


def signin(requests):
    error = None
    if requests.method == 'POST':
        username = requests.POST.get('username')
        password = requests.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(requests, user)
            return redirect(requests.GET.get('next') or '/')
        error = 'Incorrect Username or Password!'
    return render(requests, 'login.html', {'err': error, })


@login_required
def exit(requests):
    logout(requests)
    return redirect("/signin/")


@login_required
def hostlist(requests):
    return render(requests, 'hostlist.html')


@login_required
def api_host_list(requests):
    if requests.method == 'GET':
        gid = requests.GET.get('gid')
        if not gid:
            return HttpResponse(None)
        if gid == '-1':
            host_list = requests.user.account.host_user_binds.all()
        else:
            host_list = requests.user.account.host_groups.get(id=gid)
            host_list = host_list.host_user_binds.all()
        return HttpResponse(json.dumps(list(host_list.values(
            'id', 
            'host__hostname', 
            'host__ip_addr', 
            'host__port',
            'host_user__username'))))
    return HttpResponse('error requests')


@login_required
def api_host_token(requests):
    if requests.method == 'POST':
        host_id = requests.POST.get('id')
        expire_time = datetime.datetime.now() - datetime.timedelta(seconds=300)
        exist_token_obj = models.LoginToken.objects.filter(
            account_id=requests.user.account.id,
            host_user_bind_id=host_id,
            date__gt=expire_time
            ).first()
        if not exist_token_obj:
            gen_token = ''.join(
                random.sample(string.ascii_lowercase+string.digits, 8)
                )
            models.LoginToken.objects.create(
                host_user_bind_id=host_id,
                account=requests.user.account,
                val=gen_token
            )
        else:
            gen_token= exist_token_obj.val
        return HttpResponse(json.dumps({'token': gen_token}))
    return HttpResponse('error requests')

