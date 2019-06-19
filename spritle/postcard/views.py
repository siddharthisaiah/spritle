from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm
from .models import Postcard, Comment, Like
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
    title = 'Home - Postcard'
    postcards = Postcard.objects.all()
    context = {'title': title, 'postcards': postcards}
    return render(request, 'postcard/home.html', context)



# def login(request):
#     return HttpResponse("Login page")


def postcard_detail(request, pk):
    title = 'Postcard - Post'
    # TODO: wrap in try catch
    postcard = Postcard.objects.filter(id=pk)[0]
    comments = Comment.objects.filter(postcard=postcard)
    context = {'title': title, 'postcard': postcard, 'comments':comments}
    return render(request, 'postcard/detail.html', context)
