# Generated by Django 3.2.5 on 2022-10-26 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
