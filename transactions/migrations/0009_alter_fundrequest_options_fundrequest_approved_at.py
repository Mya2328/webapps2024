# Generated by Django 4.2.11 on 2024-04-28 20:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0008_remove_fundrequest_approved_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fundrequest',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='fundrequest',
            name='approved_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
