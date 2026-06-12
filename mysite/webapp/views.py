from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from webapp.models import AccountUser, ShoppingCategory, ShoppingItem, ShoppingItemsInCart, ShoppingPurchase, ShoppingPurchaseDetail, AdministratorAdmin
# from webapp.forms import UserForm

def main(request):
    return render(request, "shopping/main.html")

def searchResult(request):

    keyword = request.GET.get('keyword')
    category = request.GET.get('category')
    # context = {
    #     'keyword': keyword,
    #     'category': category,
    # }

    return render(request, "shopping/searchResult.html", {"keyword": keyword, "category": category})


# def login(request):
#     if request.session.get('is_login', None):
#         return redirect('/')
#     if request.method == 'POST':
#         login_form = forms.LoginForm(request.POST)
#         message = '入力した内容を再度確認してください'
#         if login_form.is_valid():
#             user_id = login_form.cleaned_data.get('id')
#             password = login_form.cleaned_data.get('password')
#             try:
#                 user = models.AccountUser.objects.get(user_id=user_id)
#             except:
#                 message = 'ユーザが存在しません'
#                 return render(request, 'user/login.html', locals())
#             if user.password == password:
#                 request.session['is_login']=True
#                 request.session['user_id']=user.user_id
#                 return redirect('/')
#             else:
#                 message='パスワードが正しくありません。'
#                 return render(request, 'user/login.html', locals())
#         login_form = forms.UserForm()
#         return render(request, 'user/login.html', locals())

def login(request):
    return render(request, "user/login.html")
