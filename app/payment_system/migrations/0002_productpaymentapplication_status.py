# Generated by Django 5.1.3 on 2024-11-21 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productpaymentapplication',
            name='status',
            field=models.CharField(choices=[('in_progress', 'В обработке'), ('denied', 'Отклонено'), ('accepted', 'Принято')], default='in_progress', max_length=25),
        ),
    ]
