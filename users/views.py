from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, AddressUpdateForm
from django.contrib.auth.models import User
from django.forms import ValidationError
from django import forms
from .models import *
from django.contrib.auth.models import Group
from django.views.generic import UpdateView

# Login required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from datetime import date
from orders.models import PreviousOrders
from orders.models import *

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            normal_group = Group.objects.get(name='normal')
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            normal_group.user_set.add(user)
            messages.success(
                request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/profile.html', context)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    fields = ['street_address', 'apartment_address', 'zip']

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@login_required
def favorite(request):
    user = request.user
    plants = user.favorite.all()
    context = {
        "plants": plants,
        'message': 'Favorites'
    }
    return render(request, "plant/all_plants.html", context=context)



def handler404(request, exception):
    return render(request, 'user/404.html')


def handler500(request):
    return render(request, 'user/500.html')
