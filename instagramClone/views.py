from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import Image, Profile, Comments, Likes
from .forms import ImageForm, ProfileForm, CommentForm
from django.contrib.auth.models import User
from friendship.exceptions import AlreadyExistsError
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string


# Create your views here.

def home(request):
    title = 'Instagram'
    current_user = request.user
    images = Image.get_all_images()
    comments = Comment.objects.all()
    likes = Likes.objects.all()
    profile = Profile.objects.all()
    
    return render(request, 'instagram/index.html', locals())


@login_required(login_url='/accounts/login')
def upload_image(request):
    current_user = request.user
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.profile = current_user
            upload.save()
            return redirect('edit_profile', username=request.user)
    else:
        form = ImageForm()
    
    return render(request, 'registration/upload_image.html', locals())

@login_required(login_url='/accounts/login')
def edit_profile(request, username):
    user = User.objects.get(username=username)
    try:
        profile_details = Profile.get_by_id(user.id)
    except:
        profile_details = Profile.filter_by_id(user.id)
    images = Image.get_profile_images(user.id)
    follower = len(Follow.objects.followers(user))
    following = len(Follow.objects.following(user))
    users=User.objects.all()
    users_following=Follow.objects.following(request.user)
    title = f'@{user.username} Instagram photos'

    return render(request, 'registration/edit_profile.html', locals())

@login_required(login_url='/accounts/login')
def editprofile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.user = request.user
            edit.save()
            return redirect('editprofile')
    else:
        form = ProfileForm()

    return render(request, 'registration/profile.html', locals())

@login_required(login_url='/accounts/login')
def single_image(request, image_id):
    image = Image.get_image_id(image_id)
    comments = Comments.get_comments_by_images(image_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = image
            comment.user = request.user
            comment.save()
            return redirect('single_image', image_id=image_id)
    else:
        form = CommentForm()
        
    return render(request, 'image.html', {'image':image, 'form':form, 'comments':comments})
@login_required(login_url='/accounts/login')
def search(request):
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get('search')
        profiles = Profile.search_profile(search_term)
        message = f'{search_term}'

        return render(request, 'instagram/search.html',{'message':message, 'profiles':profiles})
    else:
        message = 'Enter term to search'
        return render(request, 'instagram/search.html', {'message':message})

def comment(request,image_id):
    current_user=request.user
    profile = User.objects.get(username=current_user)
    image = Image.objects.get(id=image_id)
    comments = Comments.objects.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = image
            comment.user = current_user
            comment.save()

        return redirect('home')
    else:
        form = CommentForm()

    return render(request, 'comment.html', locals())


def follow(request,user_id):
    users=User.objects.get(id=user_id)
    follow = Follow.objects.add_follower(request.user, users)

    return redirect('/edit_profile/', locals())


def like(request, image_id):
    current_user = request.user
    image=Image.objects.get(id=image_id)
    new_like,created= Likes.objects.get_or_create(liker=current_user, image=image)
    new_like.save()

    return redirect('home')