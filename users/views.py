

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    """Register a new user."""
    if request.method != 'POST':
        form = UserRegisterForm()
    else:
        form = UserRegisterForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, new_user)
            return redirect('group_works:home')

    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    if request.method != 'POST':
        user_form = UserUpdateForm(instance=request.user)
        prof_form = ProfileUpdateForm(instance=request.user.profile)
    else:
        user_form = UserUpdateForm(request.POST, instance=request.user)
        prof_form = ProfileUpdateForm(request.POST, request.FILES,
                                      instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()

            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')

    context = {
        'user_form' : user_form,
        'prof_form' : prof_form,
        }
    return render(request, 'users/profile.html', context)

