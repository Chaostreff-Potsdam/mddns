# Generated by Django 2.2.7 on 2019-11-21 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0005_auto_20191120_2032'),
    ]

    operations = [
        migrations.RenameField(
            model_name='zone',
            old_name='owners',
            new_name='allowed_users',
        ),
    ]