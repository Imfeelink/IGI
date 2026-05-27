from django.contrib import admin

from .models import CompanyInfo, ContactEmployee, FAQ, News, PrivacyPolicy, Vacancy


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    search_fields = ('title', 'email')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'author')
    search_fields = ('title', 'short_description')
    list_filter = ('created_at',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    search_fields = ('question', 'answer')
    list_filter = ('created_at',)


@admin.register(ContactEmployee)
class ContactEmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'email')
    search_fields = ('name', 'position', 'email')
    list_filter = ('position',)


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    search_fields = ('title', 'content')


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'salary', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('is_active', 'created_at')
