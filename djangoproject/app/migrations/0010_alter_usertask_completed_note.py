# Generated by Django 5.0.6 on 2024-05-22 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_usertask_completed_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertask',
            name='completed_note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
