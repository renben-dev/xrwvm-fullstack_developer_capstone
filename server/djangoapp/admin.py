# from django.contrib import admin
# from .models import related models
from django.contrib import admin
from .models import CarMake, CarModel


# CarModelInline class — allows editing CarModels inside CarMake admin page
class CarModelInline(admin.TabularInline):  # or use admin.StackedInline
    model = CarModel
    extra = 1  # Number of empty CarModel forms to show


# CarModelAdmin class — optional customization for CarModel list view
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_type', 'year', 'car_make')
    list_filter = ('car_type', 'year', 'car_make')
    search_fields = ('name',)


# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]  # Show CarModel in CarMake admin
    list_display = ('name',)  # Assuming CarMake has a 'name' field
    search_fields = ('name',)


# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
