# Generated by Django 3.1.4 on 2020-12-21 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bigdata', '0004_auto_20201217_1406'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answercount',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('intent', models.CharField(blank=True, max_length=50, null=True)),
                ('answer', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'ANSWER_COUNT',
            },
        ),
    ]