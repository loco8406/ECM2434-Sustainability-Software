from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from .forms import ChallengeForm, WaterStationForm, CustomUserCreationForm
from .models import Challenge, UserTable
from io import BytesIO
import json
import qrcode


# User Registration
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
                    messages.warning(
                        request, "Referral code not found. No bonus points awarded.")

            # 5) Give the new user their own unique referral code
            user.getCode()

            # 6) Success message and redirect
            messages.success(request, f"Account created for {user.username}!")
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'envapp/register.html', {'form': form})


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
    # Calculate progress percentage based on user points
    level_goal = 100  # Set a fixed goal of 100 points
    raw_percentage = (request.user.points / level_goal) * \
        100 if level_goal > 0 else 0
    # Cap at 100% and round to 1 decimal
    progress_percentage = min(100, round(raw_percentage, 1))

    context = {
        'user': request.user,
        'level_goal': level_goal,
        'progress_percentage': progress_percentage,
    }
    return render(request, 'envapp/student_dashboard.html', context)


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


# Gamekeeper Dashboard
@login_required
def gamekeeper_dashboard(request):
    if request.method == 'POST':  # If the form is submitted
        challengeForm = ChallengeForm(request.POST)
        waterStationForm = WaterStationForm(request.POST)

        if challengeForm.is_valid():
            challenge = challengeForm.save()  # Save and store the challenge instance
            challenge_name = challengeForm.cleaned_data.get(
                'title')  # Get the title field
            messages.success(
                request, f'Challenge "{challenge_name}" created successfully!')
            # Redirect to the same page or another view
            return redirect('gamekeeper')

        elif waterStationForm.is_valid():
            # Save and store the waterstation instance
            waterStation = waterStationForm.save()
            waterStation_name = waterStationForm.cleaned_data.get(
                'name')  # Get the name field (or other relevant field)
            messages.success(
                request, f'Waterstation "{waterStation_name}" created successfully!')
            # Redirect to another page for the QR generation or confirmation
            return redirect('generate_qr')

    else:
        # Empty forms for GET request
        challengeForm = ChallengeForm()
        waterStationForm = WaterStationForm()

    return render(request, 'envapp/gamekeeper_dashboard.html', {'challengeForm': challengeForm, 'waterStationForm': waterStationForm})


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
def leaderboard(request):
    users = UserTable.objects.filter(role='user').order_by('-points')
    return render(request, 'envapp/leaderboard.html', {'users': users})


# Delete Account
@login_required
def delete_account(request):
    user = request.user

    Challenge.objects.filter(id=user.id).delete()

    user.delete()

    logout(request)
    messages.success(request, "Your account has been permanently deleted.")
    return redirect('login')


@login_required
def fetch_referral(request):
    if request.method == 'POST':
        user = request.user
        # Create referral code if it doesn't exist
        code = user.getCode()
        return JsonResponse({'referral_code': code})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

### QR CODE GENERATION VIEW

def generate_qr(request):
    # Default to 'https://www.example.com'
    data = request.GET.get('data', 'https://www.example.com')
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type='image/png')

#### QR CODE SCANNING VIEWS

# Load Scan QR page
@login_required
def scanQR(request):
    return render(request, 'envapp/scanqr.html')
    
# View for scanning a QR Code
def stationScanEvent(request, station_id):
    station = get_object_or_404(WaterStation, id=station_id) # Get the station that was scanned
    user = request.user # Get the current User
    user.points += station.points_reward # Add points from station to user
    user.save() # Save user
    return render(request, 'envapp/student_dashboard.html') # Redirect to User Portal