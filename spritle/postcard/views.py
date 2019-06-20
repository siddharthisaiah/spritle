from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import transaction

from .forms import SignUpForm, PostcardForm, CommentForm, ProfileForm
from .models import Postcard, Comment, Like, Profile
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
            return redirect(reverse('home'))
            
    form = SignUpForm()
    return render(request, 'postcard/signup.html', {'form': form})

@login_required
def home(request):

    title = 'Home - Postcard'
    postcards = Postcard.objects.order_by('-created_at')
    postcard_form = PostcardForm()
    postcards_user_likes = list(Like.objects.filter(user=request.user).values_list('postcard_id', flat=True)) # 

    context = {'title': title, 'postcards': postcards, 'postcard_form': postcard_form, 'postcards_user_likes': postcards_user_likes}
    
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


@login_required
def postcard_detail(request, pk):

    title = 'Postcard - Post'
    # TODO: wrap in try catch
    postcard = Postcard.objects.filter(id=pk)[0]
    comments = Comment.objects.filter(postcard=postcard)
    comment_form = CommentForm()
    postcards_user_likes = list(Like.objects.filter(user=request.user).values_list('postcard_id', flat=True))
    context = {'title': title,
               'postcard': postcard,
               'comments':comments,
               'comment_form': comment_form,
               'postcards_user_likes': postcards_user_likes}

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


@login_required
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


@login_required
def profile(request, pk):
    
    if request.user.id != pk:
        # TODO: redirect 404
        pass

    profile_instance = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile_instance)
        if form.is_valid():
            updated_profile = form.save(commit=False)
            updated_profile.user = request.user
            updated_profile.save()
            
            #Profile.objects.filter(user=request.user).update(profile_pic=profile_pic, bio=bio)

            return redirect('profile', pk=request.user.id)
    else:
        data = { 'bio': request.user.profile.bio,
                  'profile_pic': request.user.profile.profile_pic }
        form = ProfileForm(initial=data)
    return render(request, 'postcard/profile.html', {'form': form})
