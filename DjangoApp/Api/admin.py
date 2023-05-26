from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['payer', 'points', 'timestamp']
