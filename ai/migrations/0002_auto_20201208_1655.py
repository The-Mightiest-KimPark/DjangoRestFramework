# Generated by Django 3.1.2 on 2020-12-08 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grocery',
            name='reg_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]