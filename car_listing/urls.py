from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='car_list'),
    path('car/<int:car_id>/', views.detail, name='car_detail'),
]