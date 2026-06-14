from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import get_user_model

User = get_user_model()

import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import CustomUser

"""
@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        email = request.POST.get('email')
        bio = request.POST.get('bio')
        avatar = request.FILES.get('avatar')

        # update user fields
        user.email = email
        user.bio = bio

        if avatar:
            # delete old avatar if exists
            if user.avatar and os.path.isfile(user.avatar.path):
                os.remove(user.avatar.path)
            user.avatar = avatar

        user.save()
        return redirect('profile', username=user.username)
        
    return render(request, 'accounts/edit_profile.html', {'user': user})
"""
@login_required
@csrf_exempt
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        # Handle profile update
        if 'update_profile' in request.POST:
            user.email = request.POST.get('email')
            user.bio = request.POST.get('bio', '')
            if request.FILES.get('avatar'):
                user.avatar = request.FILES['avatar']
            user.save()

        # Handle password change
        elif 'change_password' in request.POST:
            old = request.POST.get('old_password')
            new = request.POST.get('new_password')
            confirm = request.POST.get('confirm_password')

            if user.check_password(old) and new == confirm:
                user.set_password(new)
                user.save()

    return render(request, 'accounts/edit_profile.html', {'user': user})
    
# Signup view
@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if password != confirm:
            return render(request, 'accounts/signup.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/signup.html', {'error': 'Username already taken'})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')

    return render(request, 'accounts/signup.html')


# Login view
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password'})

    return render(request, 'accounts/login.html')


# Logout view
def logout_view(request):
    logout(request)
    return redirect('home')

# Profile view
def profile_view(request, username):
    user = User.objects.get(username=username)
    return render(request, 'accounts/profile.html', {'profile_user': user})
    