from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from order.models import * 
from order.forms import * 
from home.models import *
from product.models import *
from user.models import UserProfile
from django.utils.crypto import get_random_string


# İyzico ödeme işlemleri için gerekli kütüphaneler


import iyzipay
import json
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import requests

api_key = 'sandbox-lsk6KUGXAVNlm4RlO5xHF1iRswAgqatz'
secret_key = 'zyJW4yAuPfXw6npQ79WtB6p1sW96Lm82'
base_url = 'sandbox-api.iyzipay.com'


options = {
    'api_key':api_key,
    'secret_key':secret_key,
    'base_url':base_url
}

sozlukToken = list()


def payment(request):
    context = dict()
   
    buyer={
        'id': 'BY789',
        'name': 'John', 
        'surname': 'Doe',
        'gsmNumber': '+905350000000',
        'email': 'email@email.com',
        'identityNumber': '74300864791',
        'lastLoginDate': '2015-10-05 12:43:35',
        'registrationDate': '2013-04-21 15:12:09',
        'registrationAddress': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        'ip': '85.34.78.112',
        'city': 'Istanbul',
        'country': 'Turkey',
        'zipCode': '34732'
    }

    address={
        'contactName': 'Jane Doe',
        'city': 'Istanbul',
        'country': 'Turkey',
        'address': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        'zipCode': '34732'
    }

    basket_items=[
        {
            'id': 'BI101',
            'name': 'Binocular',
            'category1': 'Collectibles',
            'category2': 'Accessories',
            'itemType': 'PHYSICAL',
            'price': '0.3'
        },
        {
            'id': 'BI102',
            'name': 'Game code',
            'category1': 'Game',
            'category2': 'Online Game Items',
            'itemType': 'VIRTUAL',
            'price': '0.5'
        },
        {
            'id': 'BI103',
            'name': 'Usb',
            'category1': 'Electronics',
            'category2': 'Usb / Cable',
            'itemType': 'PHYSICAL',
            'price': '0.2'
        }
    ]

    request={
        'locale': 'tr',
        'conversationId': '123456789',
        'price': '1',
        'paidPrice': '1.2',
        'currency': 'TRY',
        'basketId': 'B67832',
        'paymentGroup': 'PRODUCT',
        "callbackUrl": "http://127.0.0.1:8000/result/",
        "enabledInstallments": ['2', '3', '6', '9'],
        'buyer': buyer,
        'shippingAddress': address,
        'billingAddress': address,
        'basketItems': basket_items,
        # 'debitCardAllowed': True
    }

    checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request, options)

    #print(checkout_form_initialize.read().decode('utf-8'))
    page = checkout_form_initialize
    header = {'Content-Type': 'application/json'}
    content = checkout_form_initialize.read().decode('utf-8')
    json_content = json.loads(content)
    print(type(json_content))
    print(json_content["checkoutFormContent"])
    print("************************")
    print(json_content["token"])
    print("************************")
    sozlukToken.append(json_content["token"])
    return HttpResponse(json_content["checkoutFormContent"])


@require_http_methods(['POST'])
@csrf_exempt
def result(request):
    context = dict()

    url = request.META.get('index')

    request = {
        'locale': 'tr',
        'conversationId': '123456789',
        'token': sozlukToken[0]
    }
    checkout_form_result = iyzipay.CheckoutForm().retrieve(request, options)
    print("************************")
    print(type(checkout_form_result))
    result = checkout_form_result.read().decode('utf-8')
    print("************************")
    print(sozlukToken[0])   # Form oluşturulduğunda 
    print("************************")
    print("************************")
    sonuc = json.loads(result, object_pairs_hook=list)
    #print(sonuc[0][1])  # İşlem sonuç Durumu dönüyor
    #print(sonuc[5][1])   # Test ödeme tutarı
    print("************************")
    for i in sonuc:
        print(i)
    print("************************")
    print(sozlukToken)
    print("************************")
    if sonuc[0][1] == 'success':
        context['success'] = 'Başarılı İŞLEMLER'
        return HttpResponseRedirect(reverse('success'), context)

    elif sonuc[0][1] == 'failure':
        context['failure'] = 'Başarısız'
        return HttpResponseRedirect(reverse('failure'), context)

    return HttpResponse(url)

def success(request):
    messages.success(request, 'Ödeme Başarılı')
    return redirect('completed')
    
def fail(request):
    messages.error(request, 'Ödeme Başarısız')
    return redirect('checkout')

def completed(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    return render(request, 'completed.html', context={'setting': setting, 'category': category})

        
@login_required(login_url='login')
def addtocart(request, id):
    url = request.META.get('HTTP_REFERER') # son url'yi al
    current_user=request.user
    checkproduct = ShopCart.objects.filter(product_id=id, user = current_user) # Ürün sepette var mı sorgusu
    if checkproduct:
        control = 1 # Ürün sepette var.
    else:
        control = 0 # Ürün sepette yok.
    if request.method == 'POST': # form post edildiyse ////  detay sayfasından sepete eklendiyse burası çalışır
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1: # ürün varsa güncelle
                data = ShopCart.objects.get(product_id=id) 
                data.quantity += form.cleaned_data['quantity']
                data.save() # veritabanına kaydet
            else: # ürün yoksa ekle
                data = ShopCart() # Model ile bağlantı kur
                data.user_id = current_user.id
                data.product_id=id
                data.quantity = form.cleaned_data['quantity']
                data.save() # veritabanına kaydet
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count() # alışveriş sepetindeki öğeyi say
        messages.success(request, 'Ürün Sepetinize eklendi.')
        return HttpResponseRedirect(url)   
    else:   # detay syfasından değil de başka sayfadan (anasayfa vs.)eklendiyse burası çalışır
        if control == 1: # ürün varsa güncelle
            data = ShopCart.objects.get(product_id=id) 
            data.quantity += 1
            data.save() # veritabanına kaydet
        else: # ürün yoksa ekle
            data = ShopCart() # Model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id=id
            data.quantity = 1
            data.save() # veritabanına kaydet
        current_user=request.user
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
        messages.success(request, 'Ürün Sepetinize eklendi.')
        return HttpResponseRedirect(url)




@login_required(login_url='login')
def shoppingcart(request):
    setting = Setting.objects.get(pk=1) 
    category = Category.objects.all()
    zipcode = get_random_string(5).upper()
    current_user=request.user
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in schopcart :
        total +=  rs.product.discounted_price * rs.quantity
    return render(request, 'shoppingcart.html', context={
        'setting':setting,
        'category':category,
        'schopcart':schopcart,
        'total':total,
        'zipcode': zipcode
    })

@login_required(login_url='login')
def deleteformCart(request, id):
    ShopCart.objects.filter(id=id).delete()
    current_user=request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    messages.success(request, 'Ürün Sepetinizden silinmiştir.')
    return redirect('shoppingcart')

@login_required(login_url='login')
def favoriesadd(request, id):
    url = request.META.get('HTTP_REFERER') # son url'yi al
    current_user=request.user
    checkproduct = Favories.objects.filter(product_id=id, user = current_user) # Ürün Favorilerde var mı sorgusu
    if checkproduct:
        control = 1 # Ürün favorilerde var.
    else:
        control = 0 # Ürün favorilerde yok.
    if request.method == 'POST': # form post edildiyse ////  detay sayfasından sepete eklendiyse burası çalışır
        form = FavoriesForm(request.POST)
        if form.is_valid():
            if control == 1: # ürün varsa güncelle
                data = Favories.objects.get(product_id=id) 
                data.quantity += form.cleaned_data['quantity']
                data.save() # veritabanına kaydet
            else: # ürün yoksa ekle
                data = Favories() # Model ile bağlantı kur
                data.user_id = current_user.id
                data.product_id=id
                data.quantity = form.cleaned_data['quantity']
                data.save() # veritabanına kaydet
        request.session['favories_items'] = Favories.objects.filter(user_id=current_user.id).count() # Favorilerdeki öğeyi say 
        messages.success(request, 'Ürün Favorilerinize eklendi.')
        return HttpResponseRedirect(url)
           
    else:   # detay syfasından değil de başka sayfadan (anasayfa vs.)eklendiyse burası çalışır
        if control == 1: # ürün varsa güncelle
            data = Favories.objects.get(product_id=id) 
            data.quantity += 1
            data.save() # veritabanına kaydet
        else: # ürün yoksa ekle
            data = Favories() # Model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id=id
            data.quantity = 1
            data.save() # veritabanına kaydet
        current_user=request.user
        request.session['favories_items'] = Favories.objects.filter(user_id=current_user.id).count()
        messages.success(request, 'Ürün Favorilerinize eklendi.')
        return HttpResponseRedirect(url)


@login_required(login_url='login')
def favoriescart(request):
    setting = Setting.objects.get(pk=1) 
    category = Category.objects.all()
    current_user=request.user
    favori = Favories.objects.filter(user_id=current_user.id)
    total = 0
    for rs in favori :
        total +=  rs.product.discounted_price * rs.quantity
    return render(request, 'favories.html', context={
        'setting':setting,
        'category':category,
        'favori':favori,
        'total':total
    })


@login_required(login_url='login')
def deleteformfavories(request, id):
    Favories.objects.filter(id=id).delete()
    current_user=request.user
    request.session['favories_items'] = Favories.objects.filter(user_id=current_user.id).count()
    messages.success(request, 'Ürün Favorilerden silinmiştir.')
    return redirect('favories')


@login_required(login_url='login')
def orders(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    return render(request, 'orders.html', context={
        'category':category,
        'orders':orders,
        'setting':setting
    })


@login_required(login_url='login')
def orderdetail(request, id):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id or id.id)
    orderitem = OderProduct.objects.filter(order_id=id)
    profile = UserProfile.objects.get(user_id=current_user.id)
    return render(request, 'orderdetail.html', context={
        'category':category,
        'order':order,
        'orderitem':orderitem,
        'setting':setting,
        'profile':profile
    })

@login_required(login_url='login')
def comments(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    return render(request, 'coments.html', context={
        'category':category,
        'comments':comments,
        'setting':setting
    })

@login_required(login_url='login')
def deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(user_id=current_user.id).delete()
    messages.success(request, 'Yorumunuz Başarıyla silinmiştir.')
    return redirect('comments')


@login_required(login_url='login')
def checkout(request):
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    profile = UserProfile.objects.get(user_id=current_user.id)
    zipcode = get_random_string(5).upper()
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in schopcart :
        total +=  rs.product.discounted_price * rs.quantity
    return render(request, 'checkout.html', context={
        'setting': setting,
        'category': category,
        'profile': profile,
        'schopcart': schopcart,
        'zipcode': zipcode,
        'total': total
        })

def test_cart(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    return render(request, 'test_cart.html', context={
        'category':category,
        'setting':setting
    })