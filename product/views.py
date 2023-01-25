from django.shortcuts import render, get_object_or_404, redirect
from home.models import *
from product.models import *
from product.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

def category_products(request, slug):
    setting = Setting.objects.get(pk=1) 
    product = Product.objects.filter(category__slug = slug)
    category = Category.objects.all()
    # döngü kullanmaya gerek kalmasın diye slug ile gelen kategoriyi get ile getiriyoruz
    kategori = Category.objects.get(slug=slug)
    print(kategori)
    return render(request, 'categories.html', context={
        'setting':setting,
        'product':product,
        'category':category,
        'kategori':kategori,
    })
def campaigns_products(request, slug):
    setting = Setting.objects.get(pk=1) 
    product = Product.objects.filter(campaigns__slug = slug)
    category = Category.objects.all()
    # döngü kullanmaya gerek kalmasın diye slug ile gelen kategoriyi get ile getiriyoruz
    campaigns = Campaigns.objects.get(slug=slug)
    return render(request, 'campaigns.html', context={
        'setting':setting,
        'product':product,
        'category':category,
        'campaigns':campaigns,
    })


def detail(request, id, slug):
    setting = Setting.objects.get(pk=1) 
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    popular_products = Product.objects.all().order_by('id')[:2]
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    relevant_product = Product.objects.all()[:20]
    return render(request, 'detail.html', context={
        'setting':setting,
        'category':category,
        'product':product,
        'images':images,
        'comments':comments,
        'relevant_product':relevant_product,
        'popular_products':popular_products,
    })

def campaigns_detail(request, id, slug):
    setting = Setting.objects.get(pk=1) 
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    popular_products = Product.objects.all().order_by('id')[:2]
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    relevant_product = Product.objects.all()[:20]
    return render(request, 'campaigns_detail.html', context={
        'setting':setting,
        'category':category,
        'product':product,
        'images':images,
        'comments':comments,
        'relevant_product':relevant_product,
        'popular_products':popular_products,
    })


@login_required(login_url='login')
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user=request.user  
            data = Comment()
            data.user_id = current_user.id
            data.product_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'Yorumunuz Başarıyla Gönderilmiştir! Teşekkür Ederiz.')
            
            return HttpResponseRedirect(url)
    messages.warning(request, 'Yorum Yaparken Bir Sorunn Oluştu Lütfen Tekrar Deneyin.')
    return HttpResponseRedirect(url)   