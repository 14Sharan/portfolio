# Generated by Django 4.2.1 on 2023-05-25 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookscan', '0003_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total_price',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
