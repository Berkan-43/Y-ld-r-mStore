from django.urls import path
from user.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='signup'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('update/', user_update, name='user_update'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='change_password/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='change_password/password_reset_complete.html'),
    name='password_reset_complete'),
]