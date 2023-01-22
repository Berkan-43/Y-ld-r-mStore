from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True, upload_to='image/users/')

    class Meta:
        db_table = 'Kullanıcı_işlemleri'
        verbose_name = 'Kullanıcı_işlemleri'
        verbose_name_plural = 'Kullanıcı_işlemleri'

    def __str__(self):
        return self.user.username

    def user_name(self):
        return ' ' +self.user.first_name+ ' ' +self.user.last_name+ ' ['+self.user.username + '] ' +self.address+ ' ' +self.city+ ' ' +self.country+ ' ' +self.phone