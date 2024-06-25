# Generated by Django 4.2.6 on 2024-06-23 09:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0008_trashmedia_media_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='trashmedia',
            name='trashed_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]