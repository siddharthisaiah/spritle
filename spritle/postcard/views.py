from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import SignUpForm, PostcardForm, CommentForm
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
            return redirect('home/')
            
    form = SignUpForm()
    return render(request, 'postcard/signup.html', {'form': form})

@login_required
def home(request):

    title = 'Home - Postcard'
    postcards = Postcard.objects.all()
    postcard_form = PostcardForm()
    context = {'title': title, 'postcards': postcards, 'postcard_form': postcard_form}
    
    if request.method == 'POST':
        pc_form = PostcardForm(request.POST)
        if pc_form.is_valid():
            post = pc_form.cleaned_data['post']
            new_postcard = Postcard(user=request.user, post=post)
            new_postcard.save()

            return redirect(reverse('home'))
        else:
            # TODO: redirect 404
            pass
        
    
    return render(request, 'postcard/home.html', context)



# def login(request):
#     return HttpResponse("Login page")


def postcard_detail(request, pk):

    title = 'Postcard - Post'
    # TODO: wrap in try catch
    postcard = Postcard.objects.filter(id=pk)[0]
    comments = Comment.objects.filter(postcard=postcard)
    comment_form = CommentForm()
    context = {'title': title, 'postcard': postcard, 'comments':comments, 'comment_form': comment_form}

    if request.method == 'POST':
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            comment = c_form.cleaned_data['comment']
            new_comment = Comment(postcard=postcard, user=request.user, comment=comment)
            new_comment.save()

            return redirect('postcard_detail', pk=postcard.id)
        else:
            # TODO: redirect 404
            pass
    return render(request, 'postcard/detail.html', context)



def postcard_like(request, pk):
    if request.method == 'POST':
        next = request.POST['next']
        next = next.lstrip('/')
        if next.startswith('detail'):
            detail, pc_id = next.split('/')[:2]

        user_likes_post = Like.objects.filter(postcard__id=pk, user=request.user).count() > 0

        if user_likes_post:
            Like.objects.filter(postcard__id=pk, user=request.user).delete() # unlike
        else:
            postcard = Postcard.objects.filter(id=pk)[0]
            like = Like(postcard=postcard, user=request.user)
            like.save()

        if next != 'home/':
            return redirect('postcard_detail', pk=pc_id)
        return redirect(reverse('home'))
