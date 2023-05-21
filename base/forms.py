from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Expenses

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

# class ExpenseForm(ModelForm):
#     class Meta:
#         model = Expenses
#         fields = [
#             'intended_recipient',
#             'thing',
#             'cost',
#             'details',
#             'category',
#             'new_category',
#             'location',
#             'new_location',
#             'date_purchased'
#         ]

#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)
#     #     self.fields['category'].queryset = Expenses.objects.none()