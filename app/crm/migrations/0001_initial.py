# Generated by Django 5.1.2 on 2024-11-11 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TourPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=225)),
                ('tour', models.CharField(max_length=350)),
                ('payment_method', models.CharField(max_length=50)),
                ('payment_check', models.FileField(upload_to='media/payment_check')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
