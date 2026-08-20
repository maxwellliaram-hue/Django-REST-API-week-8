from django.contrib import admin

from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("description", "amount", "category", "owner", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("description", "owner__username")
