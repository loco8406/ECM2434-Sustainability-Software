from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import WaterStationForm
from .forms import CustomUserCreationForm
from .models import WaterStation
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache
from django.urls import reverse
import qrcode
from io import BytesIO
from django.contrib.auth.decorators import login_required

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
        waterStationForm = WaterStationForm(request.POST)
        if waterStationForm.is_valid():
            waterStation = waterStationForm.save()  # Save and store the challenge instance
            waterStation_id = waterStation.id # Get Water Station ID.
            messages.success(request, f'Water Station "{waterStation_id}" created successfully!')
            return HttpResponseRedirect(reverse('generate_qr') + f'?data={waterStation_id}')  # Redirect to the same page or another view
    else:
        form = WaterStationForm()  # Empty form for GET request
    return render(request, 'envapp/gamekeeper_dashboard.html', {'form': form})


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
def generate_qr(request):
    data = request.GET.get('data', 'https://www.example.com')  # Default to 'https://www.example.com'
    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_L,
        box_size = 10,
        border =4
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    buffer = BytesIO()
    img.save(buffer,format = "PNG")
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type='image/png')

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