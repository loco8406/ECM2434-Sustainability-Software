from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import ChallengeForm
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache
from .models import ChallengeParticipation, UserTable, Challenge
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

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
                return redirect('student_dashboard')  # Redirect to the user portal (create this view as needed)
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


def student_dashboard(request):
    return render(request, 'envapp/student_dashboard.html')

def review_submissions(request):
    submissions = ChallengeParticipation.objects.filter(reviewed=False)
    return render(request, 'review_submissions.html', {'submissions': submissions})

def mark_reviewed(request):
    if request.method == 'POST':
        submission_id = request.POST.get('submission_id')
        submission = ChallengeParticipation.objects.get(id=submission_id)
        submission.reviewed = True
        submission.save()

        # Award points
        submission.user.points += submission.challenge.points_reward
        submission.user.save()

    return redirect('review_submissions')

def challenge_list(request):
    challenges = Challenge.objects.all()
    return render(request, 'challenges/challenge_list.html', {'challenges': challenges})

@login_required
def create_challenge(request):
    if request.user.is_gamekeeper():  # Ensure only Gamekeepers can create
        if request.method == 'POST':
            form = ChallengeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('challenge_list')
        else:
            form = ChallengeForm()
        return render(request, 'challenges/create_challenge.html', {'form': form})
    else:
        return redirect('challenge_list')
        
@login_required
def edit_challenge(request, challenge_id):
    if request.user.is_gamekeeper():
        challenge = get_object_or_404(Challenge, id=challenge_id)
        if request.method == 'POST':
            form = ChallengeForm(request.POST, instance=challenge)
            if form.is_valid():
                form.save()
                return redirect('challenge_list')
        else:
            form = ChallengeForm(instance=challenge)
        return render(request, 'challenges/edit_challenge.html', {'form': form, 'challenge': challenge})
    else:
        return redirect('challenge_list')

@login_required
def delete_challenge(request, challenge_id):
    if request.user.is_gamekeeper():
        challenge = get_object_or_404(Challenge, id=challenge_id)
        challenge.delete()
    return redirect('challenge_list')