from django.contrib import admin
from .models import User, Expenses, Category, Location
# Register your models here.

# To make db models available in admin panel
admin.site.register(User)
admin.site.register(Expenses)
admin.site.register(Category)
admin.site.register(Location)
