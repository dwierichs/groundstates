# Generated by Django 2.2.7 on 2019-11-14 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20191114_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='system',
            name='wikilink',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Wikipedia link'),
        ),
    ]
