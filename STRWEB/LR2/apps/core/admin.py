from django.contrib import admin

from .models import (
    Banner,
    CompanyHistoryYear,
    CompanyInfo,
    ContactEmployee,
    FAQ,
    News,
    Partner,
    PrivacyPolicy,
    Vacancy,
)


class CompanyHistoryYearInline(admin.TabularInline):
    model = CompanyHistoryYear
    extra = 1


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    search_fields = ('title', 'email')
    inlines = [CompanyHistoryYearInline]


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_filter = ('is_active',)
    list_editable = ('is_active', 'order')


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


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website_url', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    search_fields = ('title', 'content')


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'salary', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('is_active', 'created_at')
