# Generated by Django 2.2 on 2019-05-28 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_delete_bot'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_dialog_on_top',
            field=models.BooleanField(default=True),
        ),
    ]
