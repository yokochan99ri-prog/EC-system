from django import forms
from .models import AccountUser


# class UserForm(forms.Form):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.label_suffix = ""

#     password = forms.CharField(label="パスワード", max_length=256) 
#     name = forms.CharField(label="名前", max_length=128)
#     address = forms.CharField(label="住所", max_length=256)
    

#     def clean_address(self):
#         # print("hogehogehogehoge")
#         # すでに使われているメールアドレスです
#         value = self.cleaned_data["address"]
#         if AccountUser.objects.filter(address=value).exists():
#             raise forms.ValidationError("すでに使用されているメールアドレスです")
#         return value
    
# class LoginForm(forms.Form):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.label_suffix = ""

#     password = forms.CharField(label="パスワード", max_length=256)
#     address = forms.CharField(label="住所", max_length=256)


#     def clean(self):
#         cleaned_data = super().clean()
#         address = self.cleaned_data["address"]
#         password = self.cleaned_data["password"]
#         user = AccountUser.objects.filter(address=address).first()

#         if user is None or user.password != password:
#             raise forms.ValidationError("メールアドレスまたはパスワードが間違っています")
        
#         self.user = user

#         return cleaned_data




