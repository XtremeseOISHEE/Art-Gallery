# Generated by Django 5.1.6 on 2025-04-26 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='image',
            field=models.ImageField(upload_to='artwork/'),
        ),
    ]
