# Generated by Django 4.2.11 on 2024-04-28 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_alter_fundrequest_approved_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='created_at',
        ),
    ]
