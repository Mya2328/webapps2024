# Generated by Django 4.2.11 on 2024-04-22 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundrequest',
            name='approved_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='fundrequest',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='wallettransaction',
            name='date_created',
            field=models.DateTimeField(),
        ),
    ]
