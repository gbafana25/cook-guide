# Generated by Django 4.1.7 on 2023-04-09 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_apikey_current_search'),
    ]

    operations = [
        migrations.AddField(
            model_name='apikey',
            name='item_list',
            field=models.JSONField(null=True),
        ),
    ]