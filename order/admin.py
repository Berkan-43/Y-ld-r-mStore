from django.contrib import admin
from order.models import *
# Register your models here.
@admin.register(ShopCart)
class ShopCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'product',
        'discounted_price',
        'quantity',
        'amount'
    )
    list_filter = ['user']

@admin.register(Favories)
class FavoriesAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'product',
        # 'discounted_price',
        # 'quantity',
        # 'amount'
    )
    list_filter = ['user']


class OrderProductLine(admin.TabularInline):
    model = OderProduct
    list_display = [ 
        'user',
        'product',
        'price',
        'quantitiy',
        'amount'
    ]
    can_delete = False
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display =[
        'first_name',
        'last_name',
        'phone',
        'city',
        'total',
        'status'
    ]
    list_filter = [
        'status'
    ]
    list_display_links= ('first_name',)
    # Değiştirilemeyen alanlar
    readonly_fields = (
        
        'address',
        'city',
        'country',
        'phone',
        'first_name',
        'ip',
        'last_name',
        'phone',
        'city'
    )
    inlines = [OrderProductLine]



@admin.register(OderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'product',
        'price',
        'quantity',
        'amount'
    ]
    list_filter = [
        'user'
    ]

