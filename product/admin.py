from django.contrib import admin
from product.models import *
# Register your models here.

class ProductImagesInline(admin.TabularInline):
    model = Images
    extra = 5

admin.site.register(Category)
admin.site.register(Campaigns)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'price',
        'discounted_price',
        'amount',
        'category',
    ]
        
    
    list_filter = (
        'category',
        'status',
    )

    search_fields = (
        'title',
        'price',
        'status',
    )
    inlines = [ProductImagesInline]

@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'product',
        'image',
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
        'comment',
        'status'
    )
    list_filter = (
        'status',
    )