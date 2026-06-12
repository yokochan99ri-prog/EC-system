from django.urls import path
from . import views

app_name = "webapp"

urlpatterns = [
    path('', views.main),
    path('', views.main, name='S01'),
    path('searchResult/', views.searchResult, name='S02'),
    path('cart/', views.cart, name='S04'),
    path('login/', views.login, name='M01'),
]