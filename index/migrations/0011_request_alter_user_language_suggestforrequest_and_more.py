# Generated by Django 4.2 on 2023-10-20 13:41

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models
import index.models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0010_remove_user_character_alter_user_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=500)),
                ('Content', models.TextField(max_length=2000)),
                ('Status', models.IntegerField(choices=[(0, 'WaitAccept'), (1, 'AcceptWithAdmin'), (2, 'SentSuggestion'), (3, 'Complete'), (-1, 'Canceled')], default=0)),
                ('DeadLine', django_jalali.db.models.jDateTimeField(blank=True, null=True)),
                ('RegisterTime', django_jalali.db.models.jDateTimeField(default=index.models.currentTime)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='Language',
            field=models.IntegerField(choices=[(1, 'فارسی'), (2, 'عربی')], default=1),
        ),
        migrations.CreateModel(
            name='SuggestForRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Content', models.TextField(max_length=2000)),
                ('Status', models.IntegerField(choices=[(0, 'WaitAccept'), (1, 'AcceptWithAdmin'), (2, 'Accept'), (-1, 'Reject')], default=0)),
                ('Price', models.IntegerField(default=0)),
                ('RegisterTime', django_jalali.db.models.jDateTimeField(default=index.models.currentTime)),
                ('Request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.request')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='index.user')),
            ],
        ),
        migrations.AddField(
            model_name='request',
            name='User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='index.user'),
        ),
    ]
