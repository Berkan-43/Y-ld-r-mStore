from django.urls import path
from product.views import *

urlpatterns= [
    path('category/<slug:slug>', category_products, name='category_products'),
    path('detail/<int:id>/<slug:slug>', detail, name='detail'),
    path('addcomment/<int:id>', addcomment, name='addcomment'),
]