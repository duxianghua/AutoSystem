from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import auth
#from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect

# Create your views here.
def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    path = request.POST.get('next', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        if path and path != '/auth/':
            return redirect(path)
        else:
            return redirect('/')
    else:
        return render(request,'AUTH/login.html',locals())


@login_required
def index(request):
    return render(request, 'AUTH/index.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('auth:login'))