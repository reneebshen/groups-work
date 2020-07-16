

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegisterForm


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
    return render(request, 'registration/register.html', context)
