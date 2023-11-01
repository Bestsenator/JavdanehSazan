# Generated by Django 4.2 on 2023-11-01 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0013_alter_request_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='Category',
        ),
        migrations.RemoveField(
            model_name='reservedbook',
            name='Book',
        ),
        migrations.RemoveField(
            model_name='reservedbook',
            name='User',
        ),
        migrations.AddField(
            model_name='user',
            name='Gender',
            field=models.IntegerField(choices=[(0, 'نامشخص'), (1, 'آقا'), (2, 'خانم')], default=0),
        ),
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
        migrations.DeleteModel(
            name='ReservedBook',
        ),
    ]