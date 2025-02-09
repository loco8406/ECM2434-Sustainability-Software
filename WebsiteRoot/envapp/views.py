from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import ChallengeForm, CustomUserCreationForm, VideoForm
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .models import Videos, VideoWatchers

def index(request):
    return HttpResponse("This is the index page of our app")

def register(request):
    if request.method == 'POST':  # Handle form submission
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():  # If the form is valid
            form.save()  # Save the new user
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # Redirect to login page after registration
    else:
        form = CustomUserCreationForm()  # Display an empty form for GET requests
    return render(request, 'envapp/register.html', {'form': form})

@never_cache
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Log the user in

            # Check the user's role and redirect accordingly
            if user.role == 'gamekeeper':
                return redirect('gamekeeper')  # Redirect to the gamekeeper portal
            else:
                return redirect('userPortal')  # Redirect to the user portal (create this view as needed)
        else:
            messages.error(request, 'Invalid credentials, please try again.')
            return redirect('login')
    
    return render(request, 'envapp/login.html')

def gamekeeper(request):
    if request.method == 'POST':  # If the form is submitted
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save()  # Save and store the challenge instance
            challenge_name = form.cleaned_data.get('title')  # Get the title field
            messages.success(request, f'Challenge "{challenge_name}" created successfully!')
            return redirect('gamekeeper')  # Redirect to the same page or another view
    else:
        form = ChallengeForm()  # Empty form for GET request

    return render(request, 'envapp/gamekeeper.html', {'form': form})


def admin_login(request):
    if request.method == 'POST': #If form has been submitted
        page = UserCreationForm(request.POST)
        if page.is_valid():
            page.save()
            username = page.cleaned_data('username') 
            messages.success(request, f'Account created for {username}')
            return redirect('admin')
    else:
        page = UserCreationForm()
    return render(request, 'envapp/Admin.html', {'page': page})

@login_required
def userPortal(request):
    return render(request, 'envapp/user_portal.html', {'username': request.user})

@login_required
def videoList(request):
    videos = Videos.objects.all()
    context = {'videos': videos}
    return render(request, 'envapp/videoList.html', context)

def addVideo(request):
    if request.method == 'POST': # When form submitted
        form = VideoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('videos')  # Redirect to the video list page after saving so that the gamekeeper can check it's been added
    else:
        form = VideoForm()
    return render(request, 'envapp/addVideo.html', {'form': form})
    
def videoWatchEvent(request, video_id):
    video = get_object_or_404(Videos, id=video_id)
    user = request.user
    user.points += video.videoPoints
    user.save()
    return redirect(video.videoLink)