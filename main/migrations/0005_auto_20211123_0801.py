# Generated by Django 3.2.9 on 2021-11-23 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20211122_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='ecsensorna',
            name='handlername',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ecsensorvoor',
            name='handlername',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='phsensorna',
            name='handlername',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='phsensorvoor',
            name='handlername',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sv',
            name='handlername',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
