from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('detail/<int:pk>/', views.postcard_detail, name='postcard_detail'),
    path('like/<int:pk>/', views.postcard_like, name='postcard_like'),
]
