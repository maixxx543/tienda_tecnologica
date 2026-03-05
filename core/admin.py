from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Product, Order, OrderItem

admin.site.register(User, UserAdmin)
admin.site.register(Category)
@admin.register(Product)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','price','category')
    search_fields = ('name','description','category__name_category')
    list_editable = ('price',)
    list_filter = ('name','replacement')
    exclude = ('description',)
admin.site.register(Order)
admin.site.register(OrderItem)


# Register your models here.
