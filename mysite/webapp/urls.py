from django.urls import path
from . import views

app_name = "webapp"

urlpatterns = [
    path('', views.main),
    path('', views.main, name='S01'),
    # path('login/', views.login, name='M01'),
]