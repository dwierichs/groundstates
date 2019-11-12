# Generated by Django 2.2.6 on 2019-11-12 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='system',
            name='description',
            field=models.TextField(default=None, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='system',
            name='contributors',
            field=models.TextField(default=None, verbose_name='contributors'),
        ),
    ]
