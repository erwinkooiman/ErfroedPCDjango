# Generated by Django 3.2.9 on 2021-11-22 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20211122_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='fdcontrol',
            name='handlername',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fdstatus',
            name='handlername',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
