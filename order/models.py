from django.db import models
from product.models import *
from django.contrib.auth.models import User
# Create your models here.

class ShopCart(models.Model): #ShopCart
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title
    @property
    def amount(self):
        return (self.quantity * self.product.discounted_price)

    @property
    def discounted_price(self):
        return (self.product.discounted_price)
    
    class Meta:
        db_table = 'Sepete_ekle'
        verbose_name_plural = 'Sepete_ekle'
        verbose_name = 'Sepete_ekle'

class Favories(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.user.username
    @property
    def amount(self):
        return (self.quantity * self.product.discounted_price)

    @property
    def discounted_price(self):
        return (self.product.discounted_price)
    
    class Meta:
        db_table = 'Favoriler'
        verbose_name_plural = 'Favoriler'
        verbose_name = 'Favoriler'
        
class Order(models.Model): 
    STATUS = [
        ('New', 'Yeni'),
        ('Kabul Edildi', 'Kabul Edildi'),
        ('Preaparing', 'Hazırlanıyor'),
        ('OnShihipping', 'Kargoda'),
        ('Complated', 'Tamamlanmış'),
        ('Canceled', 'İptal Edildi')
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    shopcart = models.ManyToManyField(ShopCart)
    amount = models.FloatField()
    is_it_paid = models.BooleanField(default=False, verbose_name='Ödeme Durumu')
    code =models.CharField(max_length=5, editable=False)
    first_name = models.CharField(max_length=10) # name
    last_name = models.CharField(max_length=10)  # surname
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    total = models.FloatField(default=0)
    status = models.CharField(max_length=12, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(blank=True, max_length=100)
    create_att = models.DateTimeField(auto_now_add=True)
    update_att = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.first_name = self.user.username
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = 'Siparişler-Ödemeler'
        verbose_name_plural = 'Siparişler-Ödemeler'
        verbose_name = 'Sipariş-Ödeme'

class OderProduct(models.Model): 
    STATUS = [
        ('New', 'Yeni'),
        ('Accepted', 'Kabul Edildi'),
        ('Canceled', 'İptal Edildi')
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=12, choices=STATUS, default='New')
    create_att = models.DateTimeField(auto_now_add=True)
    update_att = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title
    

