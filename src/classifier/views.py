from django.shortcuts import render
from django.contrib import auth
from .models import User

# Create your views here.

def register(request):
    if request.method == 'POST':
        # Check if contents are in proper format
        if (request.POST['username'] and request.POST['password']):
            try:
                # Check if username already exists
                user = User.objects.get(username=request.POST['username'])
                return generateJSON(301, "Invalid username"), 301
        
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password'])
                auth.login(request, user)
                return generateJSON(200, "Thanks for signing up!"), 200


def classify(request):
    pass

def login(request):
    pass

def refill(request):
    pass

def account(request):
    pass


def generateJSON(status, msg):
    return {
        "status": status,
        "msg": msg,
        "status_code": status
    }