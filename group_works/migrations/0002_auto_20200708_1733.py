# Generated by Django 3.0.8 on 2020-07-08 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_works', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='task_notes',
            new_name='notes',
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
