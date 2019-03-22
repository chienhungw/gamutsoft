from django.db import models

# Create your models here.

schedule_choices = (
("O", "Once"),
("D", "Daily"),
("W", "Weekly"),
("M", "Monthly"),
)

class Shift(models.Model):
    name = models.CharField(max_length=255, verbose_name="班次名")
    shift = models.CharField(max_length=4, choices=schedule_choices, verbose_name="班次类型")
    start_hour = models.DateTimeField(verbose_name="开始时间")
    exec_date = models.CharField(max_length=255, verbose_name="执行日期")
    message = models.CharField(max_length=255, verbose_name="发送信息")
    enabled = models.BooleanField(default=True, verbose_name="是否启用")
    def __str__(self):
        return "Shift is %s" % self.name

class WorkShift(models.Model):
    name = models.CharField(max_length=255, verbose_name="班次名")
    start_hour = models.IntegerField(verbose_name="开始时间")
    start_minute = models.IntegerField(verbose_name="开始时间")
    start_message = models.CharField(max_length=255, verbose_name="开始发送信息")
    end_hour = models.IntegerField(verbose_name="结束时间")
    end_minute = models.IntegerField(verbose_name="结束时间")
    end_message = models.CharField(max_length=255, verbose_name="结束发送信息")
    def __str__(self):
        return "Shift is %s" % self.name

class Schedule(models.Model):
    name = models.CharField(max_length=255, verbose_name="班次名")
    start_time = models.DateTimeField(verbose_name="开启时间")
    message = models.CharField(max_length=255, verbose_name="发送信息")
    enabled = models.BooleanField(default=True, verbose_name="是否启用")
    
    def __str__(self):
        return "Schedule is %s" % self.name

class ScheduleLog(models.Model):
    name = models.CharField(max_length=255, verbose_name="班次名")
    start_time = models.DateTimeField(verbose_name="开启时间")
    message = models.CharField(max_length=255, verbose_name="发送信息")
    result = models.BooleanField(default=True, verbose_name="结果")
    description = models.CharField(max_length=10000, verbose_name="详细信息") 
    def __str__(self):
        return "Schedule is %s" % self.name

class Operator(models.Model):
    name = models.CharField(max_length=255, verbose_name="用户名")
    phone = models.CharField(max_length=255, verbose_name="手机号码")

    def __str__(self):
        return "Operator is %s" % self.name


