from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm
# Create your views here.

def index(request):
    return render(request, 'postcard/index.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('postcard/home')
            
    form = SignUpForm()
    return render(request, 'postcard/signup.html', {'form': form})

@login_required
def home(request):
    return HttpResponse("Home Page")



def login(request):
    return HttpResponse("Login page")
