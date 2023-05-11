# Generated by Django 4.2 on 2023-05-02 16:02

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_artist_since'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='main_photo',
            field=models.ImageField(default='Impression/static/images/Impression_Logo.png', upload_to=users.models.user_directory_path),
        ),
    ]