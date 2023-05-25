# Generated by Django 4.2 on 2023-05-25 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_customuser_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='My Post', max_length=128)),
                ('body', models.TextField(default='The World is Violet')),
                ('image', models.ImageField(default='no_image', upload_to=users.models.user_directory_path)),
                ('alt_text', models.CharField(default='Blog Post Picture', max_length=256)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='SliderImage',
        ),
    ]