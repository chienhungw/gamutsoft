import os

import xlrd
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from apscheduler.schedulers.background import BackgroundScheduler

from schedule import forms
from . import models
# Create your views here.
from datetime import datetime, date, timedelta
from dingtalkchatbot.chatbot import DingtalkChatbot
from django.http import JsonResponse
from dingding.settings import MEDIA_ROOT


def tasks(request):
    """
    打开显示操作记录信息网页
    :param request:
    :return:
    """
    return JsonResponse({"result": "SUCCESS"})


scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, "interval", seconds=60, replace_existing=True)
def recount_job():
    """
    :return:
    """
    now = datetime.now() - timedelta(hours=8)
    now_datetime = now.strftime("%Y-%m-%d %H:%M")
    print("now date time: %s" % now_datetime)
    now_time = now.strftime("%H:%M")
    now_day, now_weekday = now.day, now.weekday()
    result_list = models.Shift.objects.filter(enabled=True)
    print(result_list)
    for shift in result_list:
        print(shift.name)
        code, message = check_shift(now_datetime, now_time, now_day, now_weekday, shift)
        if code:
            scheduler = models.ScheduleLog(name=shift.name,
                                           message=message,
                                           start_time=now,
                                           description="SUCCESS")
            scheduler.save()
            # send_message(message)


def send_message(message):
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=4da2781e03e662fc358fcd18e57f12355f667ae8c63d5e76f27dab44b4bc521e'
    xiaoding = DingtalkChatbot(webhook)
    at_mobiles = ['13476683806']
    xiaoding.send_text(msg=message, is_at_all=True)


def check_shift(now_datetime, now_time, now_day, now_weekday, shift):
    try:
        tmp = shift.exec_date.replace(" ", "").split(",")
        exec_date = []
        for tmp_1 in tmp:
            if "-" in tmp_1:
                tmp_2 = tmp_1.split("-")
                tmp_3 = range(int(tmp_2[0]), int(tmp_2[1]) + 1)
                exec_date.extend(tmp_3)
            else:
                exec_date.append(int(tmp_1))
        if shift.shift == 'O':
            print("now date time: %s, %s" % (now_datetime, shift.start_hour.strftime("%Y-%m-%d %H:%M")))
            if now_datetime == shift.start_hour.strftime("%Y-%m-%d %H:%M"):
                return True, shift.message
            else:
                return False, ""
        elif shift.shift == 'D':
            if now_time == shift.start_hour.strftime("%H:%M"):
                return True, shift.message
            else:
                return False, ""
        elif shift.shift == 'W':
            if now_time == shift.start_hour.strftime("%H:%M") and now_week in exec_date:
                return True, shift.message
            else:
                return False, ""
        elif shift.shift == 'M':
            if now_time == shift.start_hour.strftime("%H:%M") and now_day in exec_date:
                return True, shift.message
            else:
                return False, ""
        else:
            return False, ""
    except Exception as ex:
        print(ex)
        return False, ""


register_events(scheduler)
scheduler.start()


def handle_excel(file_name, flag=True):
    """
    :description 整理Excel表格获取排班信息
    :param file_name:
    :param flag:
    :return:
    """
    bk = xlrd.open_workbook(file_name)
    table = bk.sheet_by_index(0)
    date_list = table.row_values(3, start_colx=4)
    ncols = table.ncols - 3
    schedule_list = []
    print(ncols)
    if flag == True:
        models.Schedule.objects.all().delete()
    print("===========")
    for col in range(ncols):
        try:
            print(col)
            user = table.col_values(3, start_rowx=4, end_rowx=None)  # 获取操作人员信息
            schedule = table.col_values(col + 4, start_rowx=4, end_rowx=None)  # 获取排班信息
            date_now = datetime(1899, 12, 30) + timedelta(days=int(date_list[col]))
            for idx in range(len(user)):
                if schedule[idx] != "休" and schedule[idx] != "" and schedule[idx]:
                    try:
                        operator = models.Operator.objects.get(name=user[idx].strip())
                        work_shift = models.WorkShift.objects.get(name=schedule[idx])  # 获取排班信息
                        if operator and work_shift:
                            start, end, start_message, end_message = getStartAndEnd(date_now, work_shift)
                            print("success", user[idx], date_now, schedule[idx], start, end)
                            models.Schedule.objects.create(name=schedule[idx],
                                                           operator=operator,
                                                           start_time=start,
                                                           message=start_message,
                                                           enabled=True)  # 新增班信息
                            models.Schedule.objects.create(name=schedule[idx],
                                                           operator=operator,
                                                           start_time=end,
                                                           message=end_message,
                                                           enabled=True)  # 新增排班信息
                    except:
                        print("fail", user[idx], date_now, schedule[idx])

                        pass

        except IndexError:
            break
        except:
            pass


def getStartAndEnd(date_now: datetime, work_shift: models.WorkShift):
    start_message = work_shift.start_message
    end_message = work_shift.end_message
    start = date_now + timedelta(hours=work_shift.start_hour, minutes=work_shift.start_minute)
    if work_shift.start_hour > work_shift.end_hour:
        end = date_now + timedelta(days=1, hours=work_shift.end_hour, minutes=work_shift.end_minute)
    else:
        end = date_now + timedelta(hours=work_shift.end_hour, minutes=work_shift.end_minute)

    return start, end, start_message, end_message


def upload_file(request):
    """
    上传文件的request方法
    :param request:
    :return:
    """
    print("upload_file")
    if request.method == 'POST':
        form = forms.UploadFileForm(request.POST, request.FILES)  # 注意获取数据的方式
        print(MEDIA_ROOT)
        if form.is_valid():
            # filename = str(request.FILES.get("file_path")[""])
            # print(filename)
            for file in os.listdir(MEDIA_ROOT):
                print(file)
                os.remove(os.path.join(MEDIA_ROOT, file))
            form.save()
            flag = form.cleaned_data["flag"]
            handle_excel(os.path.join(MEDIA_ROOT, os.listdir(MEDIA_ROOT)[0]), flag)
            return redirect(reverse_lazy('schedule:tasks'))
    else:
        form = forms.UploadFileForm()
    return render(request, template_name='upload.html', context={'form': form})

from django.views.generic import ListView,DetailView
from rest_framework import viewsets
from . import serializer


class ScheduleView(ListView):
    model = models.Schedule
    template_name = 'schedule.html'
    # queryset = models.Schedule.objects.filter(start_time__gte=today, start_time__lt=tomorrow)

    def get_queryset(self):
        qs = super(ScheduleView, self).get_queryset()
        today = datetime.today()
        tomorrow = datetime.today() + timedelta(days=1)
        return qs.filter(start_time__gte=today, start_time__lt=tomorrow).order_by("start_time")
#
# class ScheduleView(DetailView):
#     model = models.Schedule
#     context_object_name = "blog_content"
#     template_name = "schedule.html"
#
#     # slug_field = 'slug'
#
#     def get_queryset(self):
#         qs = super(ScheduleView, self).get_queryset()
#         return qs.filter(pk=self.kwargs['pk'])


class ScheduleViewSet(viewsets.ModelViewSet):
    today = datetime.today()
    tomorrow = datetime.today() + timedelta(days=1)
    queryset = models.Schedule.objects.filter(start_time__gte=today, start_time__lt=tomorrow)
    serializer_class = serializer.ScheduleSerializer

    template_name = 'schedule.html'