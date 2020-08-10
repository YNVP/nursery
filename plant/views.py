from django.shortcuts import render, get_object_or_404, redirect
from .views import *
from .models import Plant
from orders.models import OrderPlant, Order
from nursery.models import Nursery
from .filters import PlantFilter

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import UpdateView
from django.contrib import messages
# Login required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect, HttpResponse

from .forms import PlantCreateForm
from django.db.models import Q


def all_plants(request):
    plants = Plant.objects.all()
    plant_filter = PlantFilter(request.GET, queryset=plants)

    query_list = plant_filter.qs
    # Paginating plants result

    paginator = Paginator(query_list, 12)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.get_page(page)
    except PageNotAnInteger:
        queryset = paginator.get_page(1)
    except EmptyPage:
        queryset = paginator.get_page(paginator.num_pages)

    # Sending data to page
    context = {
        "plants": queryset,
        "page_request_var": page_request_var,
        'plant_filter': plant_filter,
    }
    return render(request, 'plant/all_plants.html', context)


def nursery_plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    context = {
        'plant': plant,
    }
    return render(request, 'plant/nursery_plant_detail.html', context)


def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    context = {
        'plant': plant,
    }
    return render(request, 'plant/plant_detail.html', context)


def sow_plant(request):
    if request.method == 'POST':
        plant_form = PlantCreateForm(request.POST, user=request.user)
        if plant_form.is_valid():
            plant_form.instance.author = request.user
            plant_form.save()
            messages.success(
                request, f'Your Plant is now on sale! Checkout orders section to send plants')
            return redirect('landing_page')
    else:
        plant_form = PlantCreateForm(user=request.user)
    context = {
        'plant_form': plant_form
    }
    return render(request, 'plant/plant_form.html', context)


class PlantUpdateView(LoginRequiredMixin, UpdateView):
    model = Plant
    fields = ["description", "image", 'stock']

    def form_valid(self, form):
        print(form.instance.name)
        nursery = Nursery.objects.get(
            Q(plant__name=form.instance.name))
        form.instance.nursery = nursery
        form.save()
        return super().form_valid(form)


@login_required
def add_favorite(request):
    plant = get_object_or_404(Plant, id=request.POST.get('plant_id'))
    if plant.favorite.filter(id=request.user.id).exists():
        plant.favorite.remove(request.user)
    else:
        plant.favorite.add(request.user)
    return HttpResponse('')


@login_required
def add_to_cart(request):
    if CurrentOrder.objects.filter(user=request.user).exists():
        main_order = CurrentOrder.objects.get(user=request.user)
    else:
        main_order = CurrentOrder.objects.create(user=request.user)
    plant = get_object_or_404(Plant, id=request.POST.get('plant_id'))
    if OrderPlant.objects.filter(user=request.user, plant=plant).exists():

        order = OrderPlant.objects.get(
            user=request.user, plant=request.POST.get('plant_id'))
        order.quantity = int(request.POST.get('quantity'))
        order.nursery = plant.nursery
        order.save()
    else:
        order = OrderPlant.objects.create(
            user=request.user, plant=plant, quantity=int(request.POST.get('quantity')), nursery=plant.nursery)
    main_order.plants.add(order)
    return HttpResponse('')
