# Generated by Django 2.2.7 on 2019-11-14 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_energy_xxx'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='energy_xxx',
            name='J',
        ),
    ]
