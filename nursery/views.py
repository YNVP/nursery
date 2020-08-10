from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, NurseryRegisterForm, UserUpdateForm, NurseryUpdateForm
from django.contrib.auth.models import User
from django.forms import ValidationError
from django import forms
from plant.models import Plant
from nursery.models import Nursery
from django.contrib.auth.models import Group

from orders.models import OrderPlant, Order
from django.http import HttpResponse
# Login required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView


@login_required
def manager_home(request):
    nursery = Nursery.objects.get(user=request.user)
    plants = Plant.objects.filter(nursery=nursery)
    context = {
        'plants': plants,
    }
    return render(request, 'nursery/plants.html', context)


def nursery_detail(request, name):
    nursery = Nursery.objects.get(name=name)
    user = User.objects.get(nursery=nursery)
    plants = Plant.objects.filter(nursery=nursery)
    context = {
        'plants': plants,
        'nursery': nursery
    }
    return render(request, 'nursery/nursery_detail.html', context)


def nursery_orders(request):
    nursery = Nursery.objects.get(user=request.user)
    orders = OrderPlant.objects.filter(
        nursery=nursery, ordered=True, received=False)
    main_orders = Order.objects.all()
    print(orders)
    context = {
        'orders': orders,
    }
    return render(request, 'nursery/nursery_orders.html', context)


def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        n_form = NurseryRegisterForm(request.POST)
        if u_form.is_valid() and n_form.is_valid():
            nursery_group = Group.objects.get(name='nursery')
            u_form.save()
            username = u_form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            name = n_form.cleaned_data.get('name')
            image = n_form.cleaned_data.get('image')
            # Create Nursery
            Nursery.objects.create(name=name, image=image, manager=user)
            # Add user to nursery owner group
            nursery_group.user_set.add(user)
            messages.success(
                request, f'Your Nursery has been created successfully!')
            return redirect('nursery_login')
    else:
        u_form = UserRegisterForm()
        n_form = NurseryRegisterForm()
    context = {
        'u_form': u_form,
        'n_form': n_form
    }
    return render(request, 'nursery/registration.html', context)


class NurseryUpdateView(LoginRequiredMixin, UpdateView):
    model = Nursery
    fields = ['name', 'image']

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def add_pack_status(request):
    order = OrderPlant.objects.get(id=request.POST.get('order_id'))
    if order.packed == True:
        order.packed = False
        data = 'a'
        order.save()
    else:
        order.packed = True
        data = 'o'
        order.save()
    return HttpResponse(data)


def add_delivery_status(request):
    order = OrderPlant.objects.get(id=request.POST.get('order_id'))
    if order.being_delivered == True:
        order.being_delivered = False
        data = 'a'
        order.save()
    else:
        order.being_delivered = True
        data = 'o'
        order.save()
    return HttpResponse(data)


def add_receive_status(request):
    order = OrderPlant.objects.get(id=request.POST.get('order_id'))
    if order.received == True:
        order.received = False
        data = 'a'
        order.save()
    else:
        order.received = True

        data = 'o'
        order.save()
    return HttpResponse(data)
