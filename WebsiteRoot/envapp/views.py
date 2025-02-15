from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ChallengeForm
from .models import UserTable, VideoWatchers, Challenge


# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on user role
            if user.role == 'gamekeeper':
                return redirect('gamekeeper_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid credentials, please try again.')
            return redirect('login')

    return render(request, 'envapp/login.html')


# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')


# Student Dashboard
@login_required
def student_dashboard(request):
    return render(request, 'envapp/student_dashboard.html')


# Gamekeeper Dashboard
@login_required
def gamekeeper_dashboard(request):
    if request.method == 'POST':  # If the form is submitted
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save()
            challenge_name = form.cleaned_data.get('title')
            messages.success(
                request, f'Challenge "{challenge_name}" created successfully!')
            # Redirect to the same page
            return redirect('gamekeeper_dashboard')
    else:
        form = ChallengeForm()  # Empty form for GET request

    return render(request, 'envapp/gamekeeper_dashboard.html', {'form': form})


# User Registration
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'envapp/register.html', {'form': form})


# Settings Page
def settings_view(request):
    # Manually check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated

    if request.method == 'POST':
        user = request.user

        # Update display name
        user.first_name = request.POST.get('display_name', user.first_name)

        # Update password if provided
        new_password = request.POST.get('password')
        if new_password:
            user.set_password(new_password)

        user.save()  # Save changes in the database
        messages.success(request, 'Settings updated successfully!')

        return redirect('settings')  # Reload the settings page after saving

    return render(request, 'envapp/settings.html')


def delete_account(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Ensure user is logged in

    user = request.user

    # ✅ Fix: Use "id" instead of "userID"
    VideoWatchers.objects.filter(id=user.id).delete()  # Remove watched videos
    # Remove created challenges (if any)
    Challenge.objects.filter(id=user.id).delete()

    # Finally, delete the user account
    user.delete()

    # Log out the user after account deletion
    logout(request)
    messages.success(request, "Your account has been permanently deleted.")
    return redirect('login')
