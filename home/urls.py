from django.urls import path
from home.views import *
from django.views.generic import TemplateView
urlpatterns = [
    path('', index, name='index'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('submit/', TemplateView.as_view(template_name='success_submit.html'), name='submit'),
    path('categories/', categories, name='categories'),
    path('referance/', referance, name='referance'),
    path('about/', about, name='about'),
    path('search/', search_product, name='search'),
]