# Generated by Django 2.0.4 on 2018-04-12 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_remove_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_bio',
            field=models.TextField(blank=True, default='', null=True, verbose_name='A short bio'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_goals',
            field=models.TextField(blank=True, default='', max_length=255, null=True, verbose_name='Your current goals'),
        ),
    ]
