# Generated by Django 4.2.1 on 2023-05-26 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookscan', '0008_alter_order_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(to='bookscan.products'),
        ),
    ]