from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'property_obj', 'rating', 'created_at')
    search_fields = ('text', 'user__username', 'property_obj__title')
    list_filter = ('rating', 'created_at')
