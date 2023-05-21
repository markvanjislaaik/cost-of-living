from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (ExpenseList, ExpenseCreate, ExpenseUpdate, ExpenseDelete,
                    CustomLoginView, RegisterPage, ExpenseCreateFrom, GroupedList,
                    CategoryTotalsView, TotalsListView, UserSpendListView,
                    LocationCreate, CategoryCreate)


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('', ExpenseList.as_view(), name="expenses"),
    path('month', GroupedList.as_view(), name="month"),
    path('category-totals', CategoryTotalsView.as_view(), name="category-totals"),
    path('user-totals', TotalsListView.as_view(), name="user-totals"),
    path('user-spend', UserSpendListView.as_view(), name="user-spend"),
    path('expense-create/', ExpenseCreate.as_view(), name="expense-create"),
    path('expense-create-from/<int:pk>', ExpenseCreateFrom.as_view(), name="expense-create-from"),
    path('expense-update/<int:pk>/', ExpenseUpdate.as_view(), name="expense-update"),
    path('expense-delete/<int:pk>/', ExpenseDelete.as_view(), name="expense-delete"),
    path('location-create/', LocationCreate.as_view(), name="location-create"),
    path('category-create/', CategoryCreate.as_view(), name="category-create"),
]