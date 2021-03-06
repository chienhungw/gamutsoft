# Generated by Django 2.1.7 on 2019-03-25 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_auto_20190324_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedulelog',
            name='operator',
            field=models.CharField(default='auto', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='excel',
            name='file',
            field=models.FileField(upload_to='./media', verbose_name='上传的文件'),
        ),
        migrations.AlterField(
            model_name='excel',
            name='flag',
            field=models.BooleanField(default=True, verbose_name='是否覆盖原有数据'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='operator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedule_operator', to='schedule.Operator'),
        ),
    ]
