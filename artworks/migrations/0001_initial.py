# Generated by Django 5.1.7 on 2025-04-26 08:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(upload_to='artworks/')),
                ('category', models.CharField(choices=[('abstract', 'Abstract'), ('landscape', 'Landscape'), ('portrait', 'Portrait'), ('fantasy', 'Fantasy'), ('anime', 'Anime / Manga'), ('nature', 'Nature'), ('cityscape', 'Cityscape / Urban'), ('animals', 'Animals / Wildlife'), ('fashion', 'Fashion'), ('sports', 'Sports'), ('mythology', 'Mythology'), ('aesthetic', 'Aesthetic / Minimalism'), ('dark_art', 'Dark Art'), ('vintage', 'Vintage / Retro'), ('surreal', 'Surreal / Dreamy')], max_length=50)),
                ('art_type', models.CharField(choices=[('digital', 'Digital Art'), ('traditional', 'Traditional Art'), ('3d', '3D Art / Sculpting'), ('photography', 'Photography'), ('fanart', 'Fan Art'), ('illustration', 'Illustration'), ('concept_art', 'Concept Art'), ('pixel_art', 'Pixel Art')], default='traditional', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_available', models.BooleanField(default=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('views', models.PositiveIntegerField(default=0)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
