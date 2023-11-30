# yourapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile


def signup(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password2'])
            user.save()

            _ = UserProfile.objects.create(
                user=user,
                fullname=form.cleaned_data['fullname'],
                birthdate=form.cleaned_data['birthdate']
            ).save()
            print('success')
            return render(request, 'authentication/signup.html', {'success': True})
    else:
        form = SignUpForm()
    return render(request, 'authentication/signup.html', {'form': form})


def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to the home page or any other desired page
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})


def logout_view(request):

    if not request.user.is_authenticated:
        return redirect('home')
    
    logout(request)

    # Redirect to a specific page after logout
    return redirect('home')  # Replace 'home' with the desired URL or name of the view
