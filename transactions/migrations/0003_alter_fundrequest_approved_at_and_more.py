# Generated by Django 4.2.11 on 2024-04-22 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_alter_fundrequest_approved_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundrequest',
            name='approved_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='fundrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
