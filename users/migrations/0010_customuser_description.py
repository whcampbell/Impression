# Generated by Django 4.2 on 2023-05-23 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_message_is_friend_request_alter_message_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='description',
            field=models.TextField(default='I am an artist.'),
        ),
    ]
