from django.contrib import admin
from .models import *
admin.site.register(Products)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(ContactDetails)
# Register your models here.
