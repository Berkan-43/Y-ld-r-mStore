from django.shortcuts import render
from home.models import *
from home.forms import *
from product.models import *
from order.models import *
from django.views.generic.edit import FormView
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
# Create your views here.

def index(request):
    current_user = request.user
    setting = Setting.objects.get(pk=1)

    category2 = Category.objects.filter(parent=None)
    category = Category.objects.all()

    
    category_list = Category.objects.all().order_by('-id')[:6]
    
    just_came = Product.objects.filter(id__range =(19,41))
    trending_products = Product.objects.filter(id__range =(42,63))
    populer_products = Product.objects.filter(id__range =(64,85))
    slider_product =Product.objects.all().order_by('id')[:3]
    special_offer = Product.objects.all().order_by('-id')[:2]

    campaigns = Campaigns.objects.filter(id__range =(1,12))
    campaigns2 = Campaigns.objects.filter(id__range =(13,25))

    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    request.session['favories_items'] = Favories.objects.filter(user_id=current_user.id).count()
    return render(request, 'index.html', context={
        'setting': setting,
        'category2': category2,
        'category_list': category_list,
        'just_came': just_came,
        'trending_products': trending_products,
        'slider_product': slider_product,
        'special_offer': special_offer,
        'campaigns': campaigns,
        'campaigns2':campaigns2,
        'populer_products': populer_products,
        'category': category,
        })


class ContactFormView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/submit/'

    def form_valid(self, form):
        name = form.cleaned_data['name']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        email = form.cleaned_data['email']

        mail = EmailMessage(
            f'{name}, Tarafından Mesaj Gönderildi',
            f'Konu: {subject}\n\nEmail: {email}\n\nMesaj: {message}\n\n',
            f'"YENİ MESAJ" <{email}>', # email'in kimden (from) geldiğini yazdık.
            [settings.EMAIL_ADMIN], # email'in kime (to) gideceğini belirledik.
                reply_to=[f'{email}'], # gmail'de yanıtlama yapıldığında otomatik olarak mesaj gönderenin email adresini seçtirdik.
        )
        mail.send()
        form.save()
        messages.success(self.request, 'Mesajınız başarıyla gönderildi.')
        return super().form_valid(form)


def categories(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    return render(request, 'categories.html', context={
        'setting': setting,
        'category': category,
        })


def referance(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    category_list = Category.objects.all()[:6]
    return render(request, 'referance.html', context={
        'setting': setting,
        'category': category,
        'category_list': category_list,
        })


def about(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    return render(request, 'about.html', context={
        'setting': setting,
        'category': category,
        })

# Search
def search_product(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    products = Product.objects.all()
    query = ''
    if request.method == 'GET':
        query = request.GET.get('query')
        products = products.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__title__icontains=query) |
            Q(keywords__icontains=query) |
            Q(detail__icontains=query)
            ).distinct()
    return render(request, 'search.html', context={
        'products':products,
        'category':category,
        'query':query,
        'setting':setting
    })