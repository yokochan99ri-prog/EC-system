from django.urls import path
from . import views

app_name = "webapp"

urlpatterns = [
    path('', views.main, name='S01'),
    path('items/', views.search_result, name='S02'),
    path('items/<int:item_id>', views.ItemDetail.as_view(), name='S03'),
    path('cart/', views.cart, name='S04'),
    path('login/', views.login, name='M01'),
    path('registerUser/', views.RegisterUser.as_view(), name='M02'),
    path('registerUserConfirm/', views.register_user_confirm, name='M03'),
    path('registerUserCommit/', views.register_user_commit, name='M04'),
    path('userInfo/', views.user_info, name='M05'),
    path('updateUser/', views.updateUser.as_view(), name='M06'),
    path('updateUserConfirm/', views.update_user_confirm, name='M07'),
    path('updateUserCommit/', views.update_user_commit, name='M08'),
    path('withdrawConfirm/', views.withdrawConfirm.as_view(), name='M09'),
    # path('withdrawCommit/', views.withdraw_commit, name='M10'),
    path('logout/', views.logout, name='logout')
]