
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.db.models import Q
from . import forms, models


def main(request):  # S01
    return render(request, "shopping/main.html")


def search_result(request): # S02

    keyword = request.GET.get('keyword')
    category = request.GET.get('category')

    products = models.ShoppingItem.objects.all()

    if category:
        products = products.filter(category__name=category)

    if keyword:
        products = products.filter(
            Q(name__icontains=keyword) |
            Q(manufacturer__icontains=keyword) |
            Q(color__icontains=keyword)
        )

    context = {
        'keyword': keyword,
        'category': category,
        'products': products,
    }

    return render(request, "shopping/searchResult.html", context)


def item_detail(request, item_id):  # S03
    context = {
        "item_id": item_id,
    }
    return render(request, 'shopping/itemDetail.html', context)


def cart(request):  # S04
    return render(request, "shopping/cart.html")


def login(request): # M01
    if request.session.get('is_login', None):
        return redirect('webapp:S01')
    
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '入力した内容を再度確認してください'

        if login_form.is_valid():
            user_id = login_form.cleaned_data.get('id')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.AccountUser.objects.get(user_id=user_id)

            except:
                message = 'ユーザが存在しません'
                return render(request, 'user/login.html', locals())
            
            if user.password == password:
                request.session['is_login']=True
                request.session['user_id']=user.user_id
                return redirect('webapp:S01')
            
            else:
                message='パスワードが正しくありません。'
                return render(request, 'user/login.html', locals())
            
    login_form = forms.UserForm()
    return render(request, 'user/login.html', locals())


class RegisterUser(View):   # M02

    def get(self, request):

        form = forms.UserCreateForm()
        context = {
            "form": form,
        }
        return render(request, 'user/registerUser.html', context)

    def post(self, request):

        form = forms.UserCreateForm(request.POST)

        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "user/registerUser.html", context)
        
        request.session["register_data"] = form.cleaned_data
        return redirect('webapp:M03')


def register_user_confirm(request): # M03

    data = request.session.get('register_data')

    if not data:
        return redirect('webapp:M02')

    return render(request, "user/registerUserConfirm.html", {"data": data})


def register_user_commit(request):  # M04

    data = request.session.get('register_data')

    if not data:
        return redirect('webapp:M02')
    
    new_user = models.AccountUser()
    new_user.user_id = data['user_id']
    new_user.password = data['password']
    new_user.name = data['name']
    new_user.address = data['address']
    new_user.save()
    
    del request.session['register_data']

    return render(request, "user/registerUserCommit.html")



