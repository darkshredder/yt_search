# Generated by Django 4.0.6 on 2022-07-10 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_apikey_next_use_alter_ytsearchquery_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='next_use',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Next Use Date'),
        ),
    ]
