from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def index(request):
    return HttpResponse("This is the index page of our app")

def register(request):
    if request.method == 'POST':  # Handle form submission
        form = UserCreationForm(request.POST)
        if form.is_valid():  # If the form is valid
            form.save()  # Save the new user
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # Redirect to login page after registration
    else:
        form = UserCreationForm()  # Display an empty form for GET requests
    return render(request, 'envapp/register.html', {'form': form})