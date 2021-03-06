# Generated by Django 3.1.5 on 2021-05-11 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=10)),
                ('dob', models.CharField(max_length=55)),
                ('address', models.CharField(max_length=455)),
                ('email', models.EmailField(max_length=254)),
                ('linkedin', models.URLField(blank=True)),
                ('phone', models.CharField(max_length=10)),
                ('about', models.CharField(max_length=500)),
                ('image', models.ImageField(default='', upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyn1', models.CharField(max_length=355)),
                ('jobtitle1', models.CharField(max_length=355)),
                ('year1', models.CharField(max_length=355)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.person')),
            ],
        ),
        migrations.CreateModel(
            name='Academic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenboard', models.CharField(max_length=355)),
                ('tenmark', models.IntegerField()),
                ('twelveboard', models.CharField(max_length=355)),
                ('twelvemark', models.IntegerField()),
                ('degree', models.CharField(max_length=355)),
                ('institute', models.CharField(max_length=355)),
                ('cgpa', models.IntegerField()),
                ('exam', models.CharField(max_length=355)),
                ('rank', models.CharField(max_length=355)),
                ('gre', models.CharField(max_length=355)),
                ('course', models.CharField(max_length=355)),
                ('duration', models.CharField(max_length=355)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.person')),
            ],
        ),
    ]
