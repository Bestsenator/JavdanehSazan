# Generated by Django 4.2 on 2023-10-20 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0011_request_alter_user_language_suggestforrequest_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='Category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='index.category'),
        ),
    ]