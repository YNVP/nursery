from django.shortcuts import render, get_object_or_404
from .views import *


def landing_page(request):
    return render(request, 'users/land.html')
