# Generated by Django 2.1.7 on 2019-03-20 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Shift Name')),
                ('start_time', models.DateTimeField(verbose_name='Start Time')),
                ('message', models.CharField(max_length=255, verbose_name='Send Message')),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Shift Name')),
                ('shift', models.CharField(choices=[('O', 'Once'), ('D', 'Daily'), ('W', 'Weekly'), ('M', 'Monthly')], max_length=4, verbose_name='Shift Type')),
                ('start_hour', models.DateTimeField(verbose_name='Start Time')),
                ('exec_date', models.CharField(max_length=255, verbose_name='Start Date')),
                ('message', models.CharField(max_length=255, verbose_name='Send Message')),
                ('enabled', models.BooleanField(default=True, verbose_name='Enabled')),
            ],
        ),
    ]
