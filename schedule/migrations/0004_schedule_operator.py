# Generated by Django 2.1.7 on 2019-03-24 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_excel'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='operator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='schedule.Operator'),
        ),
    ]
