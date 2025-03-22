from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from .forms import ChallengeForm, WaterStationForm, CustomUserCreationForm
from .models import Challenge, UserTable, WaterStation, StationUsers
import qrcode
from datetime import datetime, timedelta, timezone
from io import BytesIO
import json
import os
from PIL import Image
import traceback
from django.core.exceptions import PermissionDenied
from django.utils import timezone


# LOGIN SYSTEM VIEWS
# Home Page
def home(request):
    return render(request, 'envapp/home.html')


# User Registration
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Create user object but don't save yet
            user = form.save(commit=False)
            user.bottle_size = form.cleaned_data.get('bottle_size')  # Save bottle size
            # Save user to database, which will auto-set consent_timestamp
            user.save()

            # Process referral code
            typed_code = form.cleaned_data.get('input_referral_code')
            if typed_code:
                try:
                    referrer = UserTable.objects.get(referral_code=typed_code)
                    referrer.addPoints(50)  # Reward referrer
                    user.addPoints(25)  # Reward new user
                except UserTable.DoesNotExist:
                    messages.warning(
                        request, "Referral code not found. No bonus points awarded."
                    )

            user.getCode()  # Generate referral code for the new user

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
            return render(request, 'envapp/login.html')

    return render(request, 'envapp/login.html')


# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')


# Delete Account
@login_required
def delete_account(request):
    user = request.user

    Challenge.objects.filter(id=user.id).delete()

    user.delete()

    logout(request)
    messages.success(request, "Your account has been permanently deleted.")
    return redirect('login')


# STUDENT DASHBOARD VIEWS
# Student Dashboard
@login_required
def student_dashboard(request):
    # Calculate progress percentage based on user points
    level_goal = 100  # Set a fixed goal of 100 points
    raw_percentage = (request.user.points / level_goal) * \
        100 if level_goal > 0 else 0
    # Cap at 100% and round to 1 decimal
    progress_percentage = min(100, round(raw_percentage, 1))
    user_refills = StationUsers.objects.filter(userID=request.user.id)

    context = {
        'user': request.user,
        'level_goal': level_goal,
        'progress_percentage': progress_percentage,
        'refills' : user_refills
    }
    return render(request, 'envapp/student_dashboard.html', context)


# Leaderboard
@login_required
def leaderboard(request):
    users = UserTable.objects.filter(role='user').order_by('-points')
    return render(request, 'envapp/leaderboard.html', {'users': users})


# Settings Page
def settings_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        user = request.user
        updated = False

        # Update username if provided
        new_username = request.POST.get('username')
        if new_username and new_username != user.username:
            if UserTable.objects.filter(username=new_username).exists():
                messages.error(
                    request,
                    'This username is already taken. Please choose another one.',
                    extra_tags='custom-error'
                )
                return redirect('settings')
            else:
                user.username = new_username
                updated = True

        # Update display name
        new_display_name = request.POST.get('display_name')
        if new_display_name and new_display_name != user.first_name:
            user.first_name = new_display_name
            updated = True

        # Update password
        new_password = request.POST.get('password')
        if new_password:
            user.set_password(new_password)
            update_session_auth_hash(request, user)
            updated = True

        if updated:
            user.save()
            messages.success(request, 'Settings updated successfully!')
        else:
            messages.info(request, 'No changes were made.')

        return redirect('settings')

    context = {
        'user': request.user,
        'full_name': f"{request.user.first_name} {request.user.last_name}".strip() if request.user.first_name or request.user.last_name else "No Name Provided"
    }
    return render(request, 'envapp/settings.html', context)


@login_required
def fetch_referral(request):
    if request.method == 'POST':
        user = request.user
        # Create referral code if it doesn't exist
        code = user.getCode()
        return JsonResponse({'referral_code': code})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def update_profile_picture(request):
    if request.method == "POST" and request.FILES.get("avatar"):
        user = request.user
        uploaded_image = request.FILES["avatar"]

        try:
            # Delete old profile picture if it exists (but don't delete the default image)
            if user.profile_picture and user.profile_picture.name != "profile_pics/default_profile_pic.png":
                old_picture_path = os.path.join(
                    settings.MEDIA_ROOT, str(user.profile_picture))
                if os.path.exists(old_picture_path):
                    os.remove(old_picture_path)

            # Save the new profile picture
            user.profile_picture = uploaded_image
            user.save()

            return JsonResponse({"success": True})

        except Exception as e:
            error_message = f"Error in update_profile_picture: {str(e)}"
            traceback.print_exc()  # Print full error trace in the terminal
            return JsonResponse({"success": False, "error": error_message}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


@login_required
def remove_profile_picture(request):
    if request.method == "POST":
        user = request.user

        # Delete old profile picture if it exists
        if user.profile_picture and user.profile_picture.name != "profile_pics/default_profile_pic.png":
            old_picture_path = os.path.join(
                settings.MEDIA_ROOT, str(user.profile_picture))
            if os.path.exists(old_picture_path):
                os.remove(old_picture_path)

        # Reset to default profile picture
        user.profile_picture = "profile_pics/default_profile_pic.png"
        user.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)


# GAMEKEEPER VIEWS
# Function to check if the user has the gamekeeper role
def is_gamekeeper(user):
    if user.role == "gamekeeper" and user.is_authenticated:
        return True
    raise PermissionDenied  # Show 403 Forbidden error if not a gamekeeper

# Gamekeeper Dashboard
# Handles both forms on the Gamekeeper dashboard
@login_required
@user_passes_test(is_gamekeeper, login_url='/login/')
def gamekeeper_dashboard(request):
    if request.method == 'POST':  # If the form is submitted
        challengeForm = ChallengeForm(request.POST)
        waterStationForm = WaterStationForm(request.POST)

        if challengeForm.is_valid():  # Handles challenege form if submited
            challenge = challengeForm.save()  # Save and store the challenge instance
            challenge_name = challengeForm.cleaned_data.get(
                'title')  # Get the title field
            messages.success(
                request, f'Challenge "{challenge_name}" created successfully!')
            # Redirect to the same page or another view
            return redirect('gamekeeper_dashboard')

        elif waterStationForm.is_valid():  # Handles waterstation form if submited
            # Save and store the waterstation instance
            waterStation = waterStationForm.save()  # Save and store the challenge instance
            waterStation_id = waterStation.id  # Get Water Station ID.
            print(waterStation_id)
            messages.success(
                request, f'Water Station "{waterStation_id}" created successfully!')
            # Pass data to generate_qr view to encode.
            return HttpResponseRedirect(reverse('generate_qr') + f'?data={waterStation_id}')

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
        if form.is_valid():  # Corrected method call
            form.save()
            messages.success(request, "Challenge updated successfully!")
            return redirect('gamekeeper_dashboard')
    else:
        form = ChallengeForm(instance=challenge)

    return render(request, 'envapp/edit_challenge.html', {'form': form, 'challenge': challenge})


# Delete Challenge
@csrf_exempt
def delete_challenge(request, challenge_id):
    if request.method == "POST":
        challenge = get_object_or_404(Challenge, id=challenge_id)
        challenge.delete()
        return JsonResponse({"message": "Challenge deleted successfully!"}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)


# Basic QR code generation
@login_required
def generate_qr(request):
    data = request.GET.get('data')
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


# Load Scan QR page
@login_required
def scanQR(request):
    return render(request, 'envapp/scanqr.html')


# View for scanning a QR Code
def stationScanEvent(request, station_id):
    # Get the station that was scanned
    station = get_object_or_404(WaterStation, id=station_id)
    user = request.user  # Get the current User
    # Flag used for indicating whether the user has the cooldown active.
    cooldownActive = False

    # Get all the usage records
    usageRecords = StationUsers.objects.all()

    # Get a 'cut off' time to determine if the cooldown has expired (this can be adjusted, set to 1 minute for now for ease of testing)
    cutOff = timezone.now() - timedelta(hours=1)
    print('station scanned')

    # Look through the usage records.
    for record in usageRecords:
        # If the fill record has the same user ID AND water station ID, AND that fill record is younger than the cooldown duration. (i.e this user has filled at this station within the last hour)
        if record.userID == user.id and record.waterStationID == station.id and record.fillTime > cutOff:
            cooldownActive = True  # Set the cooldown flag to true
            print(record.userID, record.waterStationID, record.fillTime, user.id, station.id, cutOff,
                  record.userID == user.id, record.waterStationID == station.id, record.fillTime > cutOff)

        # If the record's fill time is older than the cooldown duration, remove the record. This stops the database from ballooning too much with old obsolete records.
        if record.fillTime <= cutOff:
            record.delete()

    # If the cooldown isn't active, add the points.
    if cooldownActive == False:
        print('points added')
        user.points += station.points_reward # Add points from station to user's total points
        user.fuelRemaining += station.points_reward # Also add to the 'fuel' field for use in the game
        user.save() # Save user
            
        # Add a new fill record to the StationUsers table, to record that the user scanned their bottle.
        newFillRecord = StationUsers(
            userID=user.id, waterStationID=station.id, fillTime=timezone.now())
        newFillRecord.save()

    # Redirect to User Portal
    return HttpResponseRedirect(reverse('student_dashboard'))



def map_view(request):
    water_stations = WaterStation.objects.all()
    return render(request, 'envapp/map.html', {'water_stations': water_stations})


@login_required
@user_passes_test(is_gamekeeper, login_url='/login/')
def gamekeeper_map(request):
    water_stations = WaterStation.objects.all()
    if request.method == 'POST':  # If the form is submitted
        waterStationForm = WaterStationForm(request.POST, request.FILES)
        if waterStationForm.is_valid():  # Handles waterstation form if submited
            # Save and store the waterstation instance
            waterStation = waterStationForm.save()
            waterStation_name = waterStationForm.cleaned_data.get(
                'name')  # Get the name field for success message
            messages.success(
                request, f'Waterstation "{waterStation_name}" created successfully!')

            return redirect('gamekeeper_map')
        elif 'station_id' in request.POST:
            station_id = request.POST.get('station_id')
            try:
                station = WaterStation.objects.get(id=station_id)
                station.delete()
                messages.success(request, f'Water station "{station.name}" removed successfully!')
            except WaterStation.DoesNotExist:
                messages.error(request, 'Water station not found.')
    else:
        waterStationForm = WaterStationForm()
    return render(request, 'envapp/gamekeeper_map.html', {'water_stations': water_stations, 'waterStationForm': waterStationForm})

#GAME VIEWS
#Load Game
@login_required
def sippyBottle(request):
    return render(request, 'envapp/sippyBottle.html')
    
@login_required
def getUserPoints(request):
    user = request.user
    return JsonResponse({'points': user.points})

@login_required    
def updatePointsEvent(request, newPointValue):
    user = request.user # Get the current User
    
    # Check that the point value isn't being increased to prevent cheating via URL
    if newPointValue < user.points:
        user.points = newPointValue # Set new point value
        user.save()
        
    return render(request, 'envapp/student_dashboard.html') # Redirect to User Portal

def report_water_station(request, station_id):
    station = get_object_or_404(WaterStation, id=station_id)
    
    station.reports += 1
    if station.reports >= 2:  # If a station has 2 or more reports, mark as "Not Working"
        station.is_working = False

    station.save()

    messages.warning(request, f"Water station '{station.name}' has been reported as NOT WORKING.")
    return redirect('map') 

def reset_report(request, station_id):
    station = get_object_or_404(WaterStation, id=station_id)
    station.reports = 0  # Reset the report count
    station.is_working = True  # Set station back to working
    station.save()
    messages.success(request, f"Reports for '{station.name}' have been reset.")
    return redirect('gamekeeper_map')