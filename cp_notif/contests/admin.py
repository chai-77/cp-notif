from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Contest, ContestNotification


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ("name", "platform", "start_time", "notify")
    list_filter = ("platform", "notify")


@admin.register(ContestNotification)
class ContestNotificationAdmin(admin.ModelAdmin):
    list_display = ("contest", "stage", "created_at")