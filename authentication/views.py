import logging
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.decorators import login_required
from authentication.forms import UserLoginForm, UserRegisterForm
from authentication.models import User
from cart.views import merge_carts

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                user_logged_in.connect(merge_carts)
                # Redirect to the `next` parameter if present, or 'home' by default
                next_url = request.GET.get('next') or reverse('home')
                return HttpResponseRedirect(next_url)
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')


# View to list all users
def user_list(request):
    users = User.objects.all()
    return render(request, 'admin/user_list.html', {'users': users})

# View to show individual user details
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'admin/user_detail.html', {'user': user})

@login_required
def modify_user(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para modificar a los usuarios.")
    
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserRegisterForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserRegisterForm(instance=user)
    return render(request, 'admin/modify_user.html', {'form': form})