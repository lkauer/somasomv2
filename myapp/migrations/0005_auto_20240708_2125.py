# Generated by Django 2.2.7 on 2024-07-08 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20240627_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='artista',
            name='descricao',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='som',
            name='descricao',
            field=models.TextField(blank=True, null=True),
        ),
    ]