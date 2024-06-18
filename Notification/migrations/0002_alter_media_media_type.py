# Generated by Django 4.2.6 on 2024-06-12 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='media_type',
            field=models.CharField(blank=True, choices=[('archive', 'Image'), ('upload', 'Video')], max_length=20, null=True),
        ),
    ]
