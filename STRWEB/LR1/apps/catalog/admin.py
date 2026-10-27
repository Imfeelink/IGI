from django.contrib import admin

from .models import Amenity, Category, Employee, Owner, Property, Sale


class PropertyInline(admin.TabularInline):
    model = Property
    extra = 0
    fields = ('title', 'price', 'is_sold')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'birth_date')
    search_fields = ('full_name', 'email', 'phone')
    list_filter = ('birth_date',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'department')
    search_fields = ('user__username', 'position')
    list_filter = ('department',)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'owner', 'employee', 'is_sold')
    search_fields = ('title', 'description', 'characteristics')
    list_filter = ('category', 'is_sold', 'created_at')
    filter_horizontal = ('amenities',)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'property_obj', 'buyer', 'employee', 'amount', 'sale_date', 'contract_date')
    search_fields = ('property_obj__title', 'buyer__username')
    list_filter = ('sale_date', 'contract_date')
    raw_id_fields = ('property_obj', 'buyer', 'employee')
