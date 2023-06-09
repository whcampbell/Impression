# Generated by Django 4.2 on 2023-05-12 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_customuser_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_friend_request',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
