from django.shortcuts import render, get_object_or_404
from .models import Car

def list(request):
    sort_by = request.GET.get('sort_by', 'name')
    order = request.GET.get('order', 'asc')

    if order == 'asc':
        cars = Car.objects.all().order_by(sort_by)
    else:
        cars = Car.objects.all().order_by(f'-{sort_by}')

    return render(request, 'car_listing/list.html', {'cars': cars})


def detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, 'car_listing/detail.html', {'car': car})