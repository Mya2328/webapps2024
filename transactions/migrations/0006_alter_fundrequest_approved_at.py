# Generated by Django 4.2.11 on 2024-04-23 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_alter_fundrequest_approved_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundrequest',
            name='approved_at',
            field=models.DateTimeField(),
        ),
    ]