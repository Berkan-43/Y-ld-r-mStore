# Generated by Django 4.1.5 on 2023-01-30 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Sipariş-Ödeme', 'verbose_name_plural': 'Siparişler-Ödemeler'},
        ),
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='is_it_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='shopcart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.shopcart'),
        ),
        migrations.AlterModelTable(
            name='order',
            table='Siparişler-Ödemeler',
        ),
    ]
