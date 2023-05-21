from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .models import User, Expenses, Category, Location
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.forms import UserCreationForm
from .forms import MyUserCreationForm#, ExpenseForm
from django.contrib.auth import login
# from django.shortcuts import redirect
from django.db.models import Q

import datetime


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('expenses')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = MyUserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('expenses')

    def form_valid(self, form):
        print(form)
        user = form.save()
        if user:
            login(self.request, user)
        else:
            print('FAILED TO REGISTER/LOGIN')
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('expenses')
        print(self.request.user)
        return super(RegisterPage, self).get(*args, **kwargs)


class ExpenseList(LoginRequiredMixin, ListView):
    model = Expenses

    # *Leave this out if you want to default to 'object_list'
    context_object_name = 'expenses' # *

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['expenses'] = context['expenses'].filter(user=self.request.user)
        # context['count'] = context['expenses'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['expenses'] = context['expenses'].filter(
                Q(thing__icontains=search_input) |
                Q(short_tag__icontains=search_input) |
                Q(details__icontains=search_input)
            )
 
        context['search_input'] = search_input
        return context


class ExpenseCreate(LoginRequiredMixin, CreateView):
    model = Expenses
    # form_class = ExpenseForm
    # fields = '__all__'
    fields = [
        'intended_recipient',
        'thing',
        'cost',
        'details',
        'category',
        'location',
        'date_purchased'
    ]
    success_url = reverse_lazy('expenses')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['locations'] = Location.objects.all()
        return context

    def form_valid(self, form):
        print("FORM")
        # print(form)
        print(self.request.user)
        print(form.instance)
        # if form.instance.new_category:
        #     form.instance.category = Category.objects.get_or_create(name=form.instance.new_category)[0]
        # if form.instance.new_location:
        #     form.instance.location = Location.objects.get_or_create(name=form.instance.new_location)[0]
        form.instance.purchaser = self.request.user
        print(form.instance.purchaser)
        form.instance.date = str(form.instance.date_purchased)[:10]
        form.instance.year_month = str(form.instance.date_purchased)[:7]
        return super(ExpenseCreate, self).form_valid(form)


class ExpenseCreateFrom(LoginRequiredMixin, UpdateView):
    model = Expenses
    # form_class = ExpenseForm
    # fields = '__all__'
    fields = [
        'intended_recipient',
        'thing',
        'cost',
        'details',
        'category',
        # 'new_category',
        'location',
        # 'new_location',
        'date_purchased'
    ]
    success_url = reverse_lazy('expenses')

    def form_valid(self, form):
        print(self.request.user)
        form.instance.pk = None
        form.instance.new_category = Category.objects.get_or_create(name=form.instance.category)[0]
        form.instance.purchaser = self.request.user
        form.instance.date = str(form.instance.date_purchased)[:10]
        form.instance.year_month = str(form.instance.date_purchased)[:7]
        return super(ExpenseCreateFrom, self).form_valid(form)


class ExpenseUpdate(LoginRequiredMixin, UpdateView):
    model = Expenses
    # form_class = ExpenseForm
    fields = '__all__'
    success_url = reverse_lazy('expenses')


class ExpenseDelete(LoginRequiredMixin, DeleteView):
    model = Expenses
    context_object_name = 'expense'
    # fields = '__all__'
    success_url = reverse_lazy('expenses')

    # def get_queryset(self):
    #     owner = self.request.user
    #     return self.model.objects.filter(user=owner)


class GroupedList(LoginRequiredMixin, ListView):
    model = Expenses
    template_name="base/grouped_list.html"
    # context_object_name='grouped'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filter_start_date = self.request.GET.get('start-filter-area') or str((datetime.datetime.now()-datetime.timedelta(days=7)).date())
        filter_end_date = self.request.GET.get('end-filter-area') or str(datetime.datetime.now().date())
        username = self.request.GET.get('username') or ''
        
        context['expenses'] = Expenses.objects.grouped_short_tag(
            start_dt=filter_start_date,
            end_dt=filter_end_date,
            username=username
        )
        
        context['start_input'] = filter_start_date
        context['end_input'] = filter_end_date
        context['username'] = username
            
        return context


class CategoryTotalsView(LoginRequiredMixin, ListView):

    model = Expenses
    template_name = "base/category_totals_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filter_start_date = self.request.GET.get('start-filter-area') or str((datetime.datetime.now()-datetime.timedelta(days=7)).date())
        filter_end_date = self.request.GET.get('end-filter-area') or str(datetime.datetime.now().date())
        username = self.request.GET.get('username') or ''

        context['cat_totals'] = Expenses.objects.grouped_by_category(
            start_dt=filter_start_date,
            end_dt=filter_end_date,
            username=username
        )

        context['start_input'] = filter_start_date
        context['end_input'] = filter_end_date
        context['username'] = username
        return context


class TotalsListView(LoginRequiredMixin, ListView):
    model = Expenses
    template_name="base/user_totals_list.html"
    # context_object_name='grouped'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filter_start_date = self.request.GET.get('start-filter-area') or str((datetime.datetime.now()-datetime.timedelta(days=7)).date())
        filter_end_date = self.request.GET.get('end-filter-area') or str(datetime.datetime.now().date())
        
        context['user_totals'] = Expenses.objects.grouped_by_user(
            start_dt=filter_start_date,
            end_dt=filter_end_date
        )

        context['start_input'] = filter_start_date
        context['end_input'] = filter_end_date

        return context


class UserSpendListView(LoginRequiredMixin, ListView):
    model = Expenses
    template_name="base/user_spend_list.html"
    # context_object_name='grouped'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filter_start_date = self.request.GET.get('start-filter-area') or str((datetime.datetime.now()-datetime.timedelta(days=7)).date())
        filter_end_date = self.request.GET.get('end-filter-area') or str(datetime.datetime.now().date())
        
        context['user_totals'] = Expenses.objects.all_by_user(
            start_dt=filter_start_date,
            end_dt=filter_end_date
        )

        context['start_input'] = filter_start_date
        context['end_input'] = filter_end_date

        return context


class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('expenses')


class LocationCreate(LoginRequiredMixin, CreateView):
    model = Location
    fields = '__all__'
    success_url = reverse_lazy('expenses')