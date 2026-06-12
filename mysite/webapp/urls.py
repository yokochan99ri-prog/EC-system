from django.urls import path
from . import views

app_name = "webapp"

urlpatterns = [
    path('', views.main, name='S01'),
    path('searchResult/', views.searchResult, name='S02'),
    # path('login/', views.login, name='M01'),
]