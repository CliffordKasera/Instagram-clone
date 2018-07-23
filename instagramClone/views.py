from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import Image, Profile, Comments
from .forms import SignupForm, ImageForm, ProfileForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string


# Create your views here.

@login_required(login_url='/')
def home(request):
    title = 'Instagram'
    images = Image.get_all_images()
    
    return render(request, 'instagram/index.html', {'images':images,'title':title})

def signup(request):
    if request.user.is_authenticated():
        return redirect('home')
    
    else:
        form = SignupForm()
        return render(request, 'registration/registration_form.html',{'form':form})

    
def profile(request, username):
    title = 'Instagram'
    profile = User.objects.get(username=username)
    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)
    images = Image.get_profile_images(profile.id)
    title = f'@{profile.username} Instagram photos and videos'

    return render(request, 'profile/profile.html', {'title':title, 'profile':profile, 'profile_details':profile_details, 'images':images})

@login_required(login_url='/accounts/login')
def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.profile = request.user
            upload.save()
            return redirect('profile', username=request.user)
    else:
        form = ImageForm()
    
    return render(request, 'profile/upload_image.html', {'form':form})

@login_required(login_url='/accounts/login')
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.user = request.user
            edit.save()
            return redirect('edit_profile')
    else:
        form = ProfileForm()

    return render(request, 'profile/edit_profile.html', {'form':form})

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

def search(request):
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get('search')
        profiles = Profile.search_profile(search_term)
        message = f'{search_term}'

        return render(request, 'search.html',{'message':message, 'profiles':profiles})
    else:
        message = 'Enter term to search'
        return render(request, 'search.html', {'message':message})