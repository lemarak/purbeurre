# Generated by Django 3.0.8 on 2020-07-22 10:20

from django.db import migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', users.models.UserManager()),
            ],
        ),
    ]