# Generated by Django 2.0.4 on 2018-04-20 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifftasks', '0012_auto_20180412_0329'),
    ]

    operations = [
        migrations.AddField(
            model_name='ifflist',
            name='is_sticky',
            field=models.BooleanField(default=False),
        ),
    ]
