from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import *
from plant.models import Plant
# Login required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from datetime import date
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages


@login_required
def add_to_cart(request):
    if CurrentOrder.objects.filter(user=request.user).exists():
        main_order = CurrentOrder.objects.get(user=request.user)
    else:
        main_order = CurrentOrder.objects.create(user=request.user)
    plant = get_object_or_404(Plant, id=request.POST.get('plant_id'))
    order = OrderPlant.objects.create(
        user=request.user, plant=plant, quantity=int(request.POST.get('quantity')), nursery=plant.nursery)
    main_order.plants.add(order)
    plant.stock = plant.stock-int(request.POST.get('quantity'))
    return HttpResponse('')


def plant_order_detail(request, order_id):
    order = OrderPlant.objects.get(id=order_id)
    context = {
        'order': order,
    }
    return render(request, 'orders/plant_order_detail.html', context)


def orders(request):
    if CurrentOrder.objects.filter(user=request.user).exists():
        order = CurrentOrder.objects.get(user=request.user)
        if order.ordered == True:
            context = {
                'order': order,
                'checked': False,
            }
        else:
            context = {
                'order': order,
                'checked': True,
            }
    else:
        context = {
            'order': None
        }
    return render(request, 'orders/orders.html', context=context)


def checkout(request):
    if CurrentOrder.objects.filter(user=request.user).exists():
        order = CurrentOrder.objects.get(user=request.user)
        all_received = True
        small_orders = order.plants.all()
        for o in small_orders:
            if o.received == False:
                all_received = False
                break
        if order.ordered == True:
            context = {
                'order': order,
                'checked': order.ordered,
                'all_received': all_received
            }
        else:
            context = {
                'order': order,
                'checked': order.ordered,
                'all_received': all_received
            }
    else:
        context = {
            'order': None
        }
    return render(request, 'orders/checkout.html', context=context)


def confirm_checkout(request):
    if not OnDeliveryOrders.objects.filter(user=request.user).exists():
        on_delivery = OnDeliveryOrders.objects.create(user=request.user)
    else:
        on_delivery = OnDeliveryOrders.objects.get(user=request.user)
    current_order = CurrentOrder.objects.get(user=request.user)
    order = Order.objects.create(user=request.user)
    order.ordered = True
    order.shipping_address = request.user.address
    print(current_order.plants.all())
    messages.success(
        request, f'Your account has been created! You are now able to log in')
    order.plants.set(current_order.plants.all())
    small_orders = order.plants.all()
    for o in small_orders:
        o.ordered = True
        o.save()
    order.save()
    print(order.plants.all())
    on_delivery.orders.add(order)
    on_delivery.save()
    # Deleting current order
    current_order.delete()
    # Moving currentorder to running order
    return HttpResponseRedirect(reverse('on_delivery'))


def on_delivery(request):
    if OnDeliveryOrders.objects.filter(user=request.user).exists():
        on_delivery = OnDeliveryOrders.objects.get(user=request.user)
        context = {
            'on_delivery': on_delivery
        }
    else:
        context = {
            'on_delivery': None
        }
    return render(request, 'orders/on_delivery.html', context)


def previous_orders(request):
    if PreviousOrders.objects.filter(user=request.user).exists():
        previous_orders = PreviousOrders.objects.get(user=request.user)
        context = {
            'orders': previous_orders.orders.all(),
        }
    else:
        previous_orders = PreviousOrders.objects.create(user=request.user)
        context = {
            'orders': None
        }
    return render(request, 'orders/previous_orders.html', context)


def save_order(request):
    user_order = Order.objects.get(
        id=request.POST.get('order_id'))
    print(user_order)
    if PreviousOrders.objects.filter(user=request.user).exists():
        previous_order = PreviousOrders.objects.get(
            user=request.user)
    else:
        previous_order = PreviousOrders.objects.create(
            user=request.user)
    previous_order.orders.add(user_order)
    return HttpResponse('')


def delete_item(request):
    order_item = OrderPlant.objects.get(
        id=request.POST.get('order_id'))
    order_item.delete()
    return HttpResponse('')


def delete_order(request):
    user_order = Order.objects.get(
        id=request.POST.get('order_id'))
    inner_orders = user_order.plants.all()
    for o in inner_orders:
        o.delete()
    user_order.delete()
    return HttpResponse('')
