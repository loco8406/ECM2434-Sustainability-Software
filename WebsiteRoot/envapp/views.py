from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import CustomUserCreationForm, ChallengeForm
from .models import Challenge, UserTable


# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

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
    challenges = Challenge.objects.all()
    return render(request, 'envapp/student_dashboard.html', {'challenges': challenges})


# Gamekeeper Dashboard
@login_required
def gamekeeper_dashboard(request):
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save()
            messages.success(
                request, f'Challenge "{challenge.title}" created successfully!')
            return redirect('gamekeeper_dashboard')
    else:
        form = ChallengeForm()

    challenges = Challenge.objects.all().order_by('-created_at')
    return render(request, 'envapp/gamekeeper_dashboard.html', {'form': form, 'challenges': challenges})


# Edit Challenge
@login_required
def edit_challenge(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)

    if request.method == 'POST':
        form = ChallengeForm(request.POST, instance=challenge)
        if form.is_valid():
            form.save()
            messages.success(request, "Challenge updated successfully!")
            return redirect('gamekeeper_dashboard')
    else:
        form = ChallengeForm(instance=challenge)

    return render(request, 'envapp/edit_challenge.html', {'form': form, 'challenge': challenge})


# Delete Challenge
@csrf_exempt  # Only use this if CSRF token isn't passed properly
def delete_challenge(request, challenge_id):
    if request.method == "POST":
        challenge = get_object_or_404(Challenge, id=challenge_id)
        challenge.delete()
        return JsonResponse({"message": "Challenge deleted successfully!"}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)


# Leaderboard
@login_required
@login_required
def leaderboard(request):
    users = UserTable.objects.filter(role='user').order_by('-points')
    return render(request, 'envapp/leaderboard.html', {'users': users})


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
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        user = request.user

        user.first_name = request.POST.get('display_name', user.first_name)

        new_password = request.POST.get('password')
        if new_password:
            user.set_password(new_password)

        user.save()
        messages.success(request, 'Settings updated successfully!')

        return redirect('settings')

    return render(request, 'envapp/settings.html')


# Delete Account
@login_required
def delete_account(request):
    user = request.user

    Challenge.objects.filter(id=user.id).delete()

    user.delete()

    logout(request)
    messages.success(request, "Your account has been permanently deleted.")
    return redirect('login')
