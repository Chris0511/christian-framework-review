# Generated by Django 5.0.4 on 2024-09-17 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ais', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='nim',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='teachers',
            name='nip',
            field=models.CharField(max_length=255),
        ),
    ]
