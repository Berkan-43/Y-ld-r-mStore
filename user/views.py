from django.shortcuts import render, redirect
from user.forms import *
from user.models import *
from home.models import *
from product.models import *
from django.contrib.auth import login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import FormView
from .tokens import account_activate_token
from django.conf import settings
from django.contrib.auth.views import PasswordResetView


class RegisterUser(SuccessMessageMixin, FormView):
    form_class = CustomUserCreationForm
    template_name = 'sign_up.html'
    success_url = reverse_lazy('index')
    success_message = "Kaydınız Tamamlandı. Hesabınızı etkinleştirmek için e-posta'nızı (spam klasörünüzü) kontrol edin!"

    def form_valid(self, form):
        user = form.save(commit=True)

        mail_subject = 'Oturum açmadan önce. Hesabınızı etkinleştirin.'
        current_site = get_current_site(self.request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activate_token.make_token(user)
        link_dict = {'url': reverse('activate', kwargs={'uidb64': uid, 'token': token})}
        link = f"http://{get_current_site(self.request).domain}{link_dict.get('url')}"

        message = render_to_string('activate_account.html', {
            'user': user, 'domain': current_site.domain,
            'uid': uid, 'token': token
        })
        email = send_mail(mail_subject, message, settings.EMAIL_HOST_USER, (user.email,),
                          fail_silently=True)
        print('success\n', link) if email else print('Ters giden birşey mi var?')
        return super().form_valid(form)

class LoginUserView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_message = 'Sisteme başarıyla giriş yaptınız! '

class ActivateView(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, TypeError, ValueError, OverflowError):
            user = None
        if user is not None and account_activate_token.check_token(user=user, token=token):
            user.is_active = True
            user.save()
            login(request=request, user=user)
            messages.add_message(request, messages.INFO, 'Hesabınızı başarıyla etkinleştirdiniz')
            return redirect('index')
        else:
            return HttpResponse('bağlantı geçersiz üzgünüm!')


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, 'Başarıyla Çıkış Yaptınız.')
    return redirect('/')


@login_required(login_url='login')
def profile(request):
    setting = Setting.objects.get(pk=1) 
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    return render(request, 'profile.html', context={
        'setting':setting,
        'category':category,
        'profile':profile
    })


@login_required(login_url='login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance= request.user) # istek kullanıcının, kullanıcı oturum verileridir
        # "örnek = request.user.userprofile", 'userprofile' modelinden gelir -> OnetoOneField ilişkisi
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profiliniz başarıyla güncellendi.')
            return redirect('profile')

    else:
        category= Category.objects.all()
        current_user=request.user # Kullanıcı oturumu Bilgilerine Erişim
        user_form = UserUpdateForm(instance= request.user)
        profile_form= ProfileUpdateForm(instance= request.user.userprofile) # 'userprofile' modeli -> kullanıcıyla OnetoOneField ilişkisi
        
        return render(request, 'user_update.html', context={
            'category':category,
            'profile_form':profile_form,
            'user_form':user_form
        })


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'change_password/password_reset.html'
    email_template_name = 'change_password/password_reset_email.html'
    subject_template_name = 'change_password/password_reset_subject.txt'
    success_message = "Girdiğiniz e-postaya sahip bir hesap varsa,  " \
                      "şifrenizi ayarlamanız için size talimatları e-posta ile gönderdik. Onları kısa süre içinde almalısınız." \
                      " Bir e-posta almazsanız, " \
                      "lütfen kayıt olduğunuz adresi girdiğinizden emin olun ve spam klasörünüzü kontrol edin."
    success_url = reverse_lazy('index')


