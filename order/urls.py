from django.urls import path
from order.views import *

urlpatterns = [       
    path('addtocart/<int:id>', addtocart, name='addtocart'),    
    path('shoppingcart/', shoppingcart, name='shoppingcart'),    
    path('deleteformCart/<int:id>', deleteformCart, name='deleteformCart'),
    path('favoriesadd/<int:id>', favoriesadd, name='favoriesadd'),    
    path('favories/', favoriescart, name='favories'),    
    path('deleteformfavories/<int:id>', deleteformfavories, name='deleteformfavories'),       
    path('orders/', orders, name='orders'),    
    path('orderdetail/<int:id>', orderdetail, name='orderdetail'),    
    path('comments/', comments, name='comments'),    
    path('deletecomment/<int:id>', deletecomment, name='deletecomment'),  
    path('checkout/', checkout, name='checkout'),
    path('completed/', completed, name='completed'),
    path('test_cart/', test_cart, name='test_cart'),
    path('payment/', payment, name='payment'),
    path('result/', result, name='result'),
    path('success/', success, name='success'),
    path('failure/', fail, name='failure'),
]