
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.db.models import Q
from . import forms, models


def main(request):  # S01

    is_login = request.session.get('is_login', False)
    if request.session.get('user_id', None):
        user_id = request.session.get('user_id')
        user = models.AccountUser.objects.get(user_id=user_id)
    else:
        user = None

    context = {
        'is_login': is_login,
        'user': user,
    }

    return render(request, "shopping/main.html", context)

def logout(request):
    if request.session.get('is_login', None):
        request.session.flush()
        return redirect(reverse('webapp:M01'))
    return redirect(reverse('webapp:S01'))

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

class ItemDetail(View): # S03

    def get(self, request, item_id):

        product = models.ShoppingItem.objects.get(item_id=item_id)
        stock = product.stock
        is_login = request.session.get('is_login', False)
        
        if stock < 1:
            on_sale = False
            quantities = 0
        else:
            on_sale = True
            quantities = range(1, stock+1)

        return render(request, 'shopping/itemDetail.html', locals())
    
    def post(self, request, item_id):

        product = models.ShoppingItem.objects.get(item_id=item_id)
        quantity = request.POST.get('quantity')
        user_id = request.session.get('user_id')

        item_incart = models.ShoppingItemsInCart(
            amount=quantity,
            item=product,
            user_id=user_id
        )

        item_incart.save()

        return redirect(reverse('webapp:S04'))

def cart(request):  # S04
    # if not request.session.get("is_login", None):
    #     return redirect(reverse('webapp:M01'))
    user_id = request.session.get('user_id')
    cart_items = models.ShoppingItemsInCart.objects.filter(user_id = user_id).select_related('item')
    total_cost = 0
    for cart in cart_items:
        total_cost += cart.item.price * cart.amount

    context = {
        "cart_items": cart_items,
        "total_cost": total_cost,

    }

    return render(request, "shopping/cart.html", context)

def login(request): # M01
    if request.session.get('is_login', None):
        return redirect(reverse('webapp:S01'))
    
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '入力した内容を再度確認してください'

        if login_form.is_valid():
            user_id = login_form.cleaned_data.get('id')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.AccountUser.objects.get(user_id=user_id)

            except:
                message = 'ユーザーが存在しません'
                return render(request, 'user/login.html', locals())
            
            if user.password == password:
                request.session['is_login']=True
                request.session['user_id']=user.user_id
                return redirect(reverse('webapp:S01'))
            
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
            return render(request, "user/registerUser.html", {"form": form})

        return render(request, "user/registerUserConfirm.html", {"form": form})

def register_user_confirm(request): # M03

    if request.method != "POST":
        return redirect(reverse("webapp:M02"))
    
    form = forms.UserCreateForm(request.POST)

    if not form.is_valid():
        return render(request, "user/registerUser.html", {"form": form})
    
    return render(request, "user/registerUserConfirm.html", {"form": form})

def register_user_commit(request):  # M04

    if request.method != "POST":
        return redirect(reverse('webapp:M02'))
    
    form = forms.UserCreateForm(request.POST)

    if not form.is_valid():
        return render(request, "user/registerUser.html", {"form": form})
    
    new_user = models.AccountUser()
    new_user.user_id = form.cleaned_data['user_id']
    new_user.password = form.cleaned_data['password']
    new_user.name = form.cleaned_data['name']
    new_user.address = form.cleaned_data['address']
    new_user.save()
    request.session["is_login"] = True
    request.session["user_id"] = new_user.user_id

    return render(request, "user/registerUserCommit.html", {"new_user": new_user})

def user_info(request): # M05
    if not request.session.get("is_login", None):
        return redirect(reverse('webapp:M01'))
    user_id = request.session.get("user_id")
    user = models.AccountUser.objects.get(user_id=user_id)

    return render(request, 'user/userInfo.html', {"user": user})

class updateUser(View):  # M06

    def get(self, request):
        if not request.session.get("is_login", None):
            return redirect(reverse('webapp:M01'))
        user_id = request.session.get('user_id')
        user = models.AccountUser.objects.get(user_id=user_id)
        form = forms.UserUpdateForm(instance=user)

        return render(request, "user/updateUser.html", {"user": user, "form": form})

    def post(self, request):
        if not request.session.get("is_login", None):
            return redirect(reverse('webapp:M01'))
        user_id = request.session.get('user_id')
        user = models.AccountUser.objects.get(user_id=user_id)
        form = forms.UserUpdateForm(request.POST, instance=user)

        if not form.is_valid():
            return render(request, "user/updateUser.html", {"user": user, "form": form})

        return render(request, "user/updateUserConfirm.html", {"user": user, "form": form})

def update_user_confirm(request):   # M07
    if not request.session.get("is_login", None):
            return redirect(reverse('webapp:M01'))
    return redirect(reverse("webapp:M06"))

def update_user_commit(request):    # M08
    
    if request.method != "POST":
        return redirect(reverse('webapp:M06'))
    
    if not request.session.get("is_login", None):
        return redirect(reverse("webapp:M01"))

    user_id = request.session.get('user_id')
    user = models.AccountUser.objects.get(user_id=user_id) 
    user.name = request.POST.get("name")
    user.address = request.POST.get("address")

    if request.POST.get("password"):
        user.password = request.POST.get("password")

    if user.user_id != request.POST.get("user_id"):
        previous_user = models.AccountUser.objects.get(user_id=user.user_id)
        user.user_id = request.POST.get("user_id")
        previous_user.delete()
    else:
        user.user_id = request.POST.get("user_id")

    user.save()
    request.session["user_id"] = user.user_id

    # user_id = request.session.get('user_id')
    # update_user = models.AccountUser.objects.get(user_id=user_id)
    # form = forms.UserUpdateForm(request.POST, instance=update_user)

    # if not form.is_valid():
    #     return render(request, "user/updateUserConfirm.html", {"form": form, "user": update_user})

    # update_user = form.save(commit=False)
    # password = form.cleaned_data.get("password")

    # if password:
    #     update_user.password = password

    # update_user.save()

    return render(request, 'user/updateUserCommit.html', {"user": user})

class withdrawConfirm(View):    # M09

    def get(self, request):

        user_id = request.session.get('user_id')
        name = models.AccountUser.objects.get(user_id=user_id)

        return render(request, "user/withdrawConfirm.html", {"name": name})
    
    def post(self, request):

        user_id = request.session.get('user_id')
        user = models.AccountUser.objects.get(user_id=user_id)
        name = user.name
        user.delete()
        request.session.flush()

        return render(request, "user/withdrawCommit.html", {"name": name})

# def withdraw_commit(request):   # M10
#     return render(request, 'user/withdrawCommit.html')