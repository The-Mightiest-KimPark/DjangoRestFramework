# Generated by Django 3.1.2 on 2020-12-12 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('refrigerator', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='refrigerator',
            old_name='motion_sensor_on_off',
            new_name='outing_mode',
        ),
    ]
