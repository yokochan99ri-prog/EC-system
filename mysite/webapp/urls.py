from django.urls import path
from . import views

app_name = "webapp"

urlpatterns = [
    path('', views.main),
    path('', views.main, name='S01'),
    path('searchResult/', views.search_result, name='S02'),
    path('cart/', views.cart, name='S04'),
    path('login/', views.login, name='M01'),
    path('registerUser/', views.RegisterUser.as_view(), name='M02'),
    path('registerUserConfirm/', views.register_user_confirm, name='M03'),
    path('registerUserCommit/', views.register_user_commit, name='M04'),
]