# Generated by Django 5.1.5 on 2025-01-25 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcontent',
            name='image_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
