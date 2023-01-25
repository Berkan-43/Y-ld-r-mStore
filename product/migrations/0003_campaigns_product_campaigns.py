# Generated by Django 4.1.5 on 2023-01-25 12:30

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_product_category_delete_populermodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaigns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('keywords', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Kampanya',
                'verbose_name_plural': 'Kampanyalar',
                'db_table': 'Kampanyalar',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='campaigns',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='campaigns_product', to='product.campaigns'),
        ),
    ]
