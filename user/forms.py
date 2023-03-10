from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm 
from django.contrib.auth.models import User
from user.models import UserProfile
from django.forms import TextInput, FileInput, Select, EmailInput, PasswordInput
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            'username', 'email', 'password1', 'password2'
        ]

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data.get('email')).exists():
            raise forms.ValidationError('Bu e-posta sistemde zaten var')
        return self.cleaned_data['email']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.email = self.cleaned_data.get('email')
            user.is_active = False
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name'
        )
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
        
            field.widget.attrs.update({'class': 'form-control col-12'}),
            field.widget.attrs.update({'class': 'form-control col-12'}),
            field.widget.attrs.update({'class': 'form-control col-12'}),
            field.widget.attrs.update({'class': 'form-control col-12'}),

CITY = [
    ('Bir Se??im Yap??n', 'Bir Se??im Yap??n'),
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('Izmir', 'Izmir'),
    ('Bal??kesir', 'Bal??kesir'),
    ('Antalya', 'Antalya'),
    ('Adana', 'Adana'),
    ('Trabzon', 'Trabzon'),
    ('Ad??yaman', 'Ad??yaman'),
    ('Bursa', 'Bursa'),
    ('Bilecik', 'Bilecik'),
    ('K??tahya', 'K??tahya'),
    ('Hatay', 'Hatay'),
    ('Ayd??n', 'Ayd??n'),
    ('Erzurum', 'Erzurum'),
    ('Konya', 'Konya'),
    ('Edirne', 'Edirne'),
    ('Kayseri', 'Kayseri'),
    ('Eski??ehir', 'Eski??ehir'),
    ('Kahramanmara??', 'Kahramanmara??'),
    ('AfyonKarahisar', 'AfyonKarahisar'),
    ('Gaziantep', 'Gaziantep'),
]
#  Profil g??ncelleme formu
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'phone',
            'address',
            'city',
            'country',
            'image'
        )
        widgets = {
            'phone'   : TextInput(attrs={'class':'form-control'}),
            'address'   : TextInput(attrs={'class':'form-control'}),
            'city'   : Select(attrs={'class':'form-control'}, choices=CITY),
            'country'   : TextInput(attrs={'class':'form-control'}),
            'image'   : FileInput(attrs={'class':'form-control'})
        }


# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = (
#             'phone',
#             'address',
#             'city',
#             'country',
#             'image'
#         )

#     def __init__(self, *args, **kwargs):
#         super(UserProfileForm, self).__init__(*args, **kwargs)
#         for name, field in self.fields.items():
        
#             field.widget.attrs.update({'class': 'form-control col-12'}),
#             field.widget.attrs.update({'class': 'form-control col-12'}),
#             field.widget.attrs.update({'class': 'form-control col-12'}),
#             field.widget.attrs.update({'class': 'form-control col-12'}),