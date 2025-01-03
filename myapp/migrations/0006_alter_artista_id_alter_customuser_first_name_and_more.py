# Generated by Django 5.1.2 on 2024-10-26 20:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20240708_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artista',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='som',
            name='audio',
            field=models.FileField(blank=True, null=True, upload_to='audios/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp3'])]),
        ),
        migrations.AlterField(
            model_name='som',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
