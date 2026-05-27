from django.contrib import admin

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'birth_date', 'timezone')
    search_fields = ('user__username', 'phone')
    list_filter = ('timezone',)
