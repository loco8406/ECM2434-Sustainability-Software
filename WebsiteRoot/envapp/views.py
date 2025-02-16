from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import ChallengeForm
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .models import UserTable


def index(request):
    return HttpResponse("This is the index page of our app")

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # 1) Create the user object, but don't save it yet
            user = form.save(commit=False)

            # 2) Save the user so we have a primary key
            user.save()

            # 3) Read the typed referral code from the form
            typed_code = form.cleaned_data.get('input_referral_code')

            # 4) If they entered a code, see if it matches a referrer
            if typed_code:
                try:
                    referrer = UserTable.objects.get(referral_code=typed_code)
                    # Reward both
                    referrer.addPoints(50)  # e.g., 50 points for referrer
                    user.addPoints(25)      # e.g., 25 points for new user
                except UserTable.DoesNotExist:
                    messages.warning(request, "Referral code not found. No bonus points awarded.")

            # 5) Give the new user their own unique referral code
            user.getCode()

            # 6) Success message and redirect
            messages.success(request, f"Account created for {user.username}!")
            return redirect('login')
    else:
        form = CustomUserCreationForm()

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
    # Calculate progress percentage based on user points
    level_goal = 100  # Set a fixed goal of 100 points
    raw_percentage = (request.user.points / level_goal) * 100 if level_goal > 0 else 0
    progress_percentage = min(100, round(raw_percentage, 1))  # Cap at 100% and round to 1 decimal

    context = {
        'user': request.user,
        'level_goal': level_goal,
        'progress_percentage': progress_percentage,
    }
    return render(request, 'envapp/student_dashboard.html', context)


@login_required
def fetch_referral(request):
    if request.method == 'POST':
        user = request.user
        # Create referral code if it doesn't exist
        code = user.getCode()
        return JsonResponse({'referral_code': code})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)