from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Client, Trener, Address, Group, Payment)
class ClientAdmin(admin.ModelAdmin):
    pass