from django.shortcuts import render
from django.contrib.auth import authenticate, login

def signin(request):
    return render(request, 'signin.html')

def auth_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return render(request, 'landing.html', {
            'username': username
        })
    return render(request, 'signin.html', {
        'error_message': 'incorrect credentials'
    })

def index(request):
    if request.user.is_authenticated:
        return logged_in(request)
    return login(request)

def login(request):
    render()

def login_auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return logged_in(request)
    

def logged_in(request):
