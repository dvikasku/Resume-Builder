# Generated by Django 3.1.5 on 2021-05-15 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experience',
            name='person',
        ),
        migrations.DeleteModel(
            name='Academic',
        ),
        migrations.DeleteModel(
            name='Experience',
        ),
    ]
