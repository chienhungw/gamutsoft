from django.shortcuts import render

from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from apscheduler.schedulers.background import BackgroundScheduler
from . import models
# Create your views here.
from datetime import datetime, date, timedelta
from dingtalkchatbot.chatbot import DingtalkChatbot
from django.http import JsonResponse


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
            scheduler = models.ScheduleLog(name = shift.name,
                                         message = message,
                                         start_time = now,
                                         description = "SUCCESS")
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
                tmp_3 = range(int(tmp_2[0]), int(tmp_2[1])+1)
                exec_date.extend(tmp_3)
            else:
                exec_date.append(int(tmp_1))
        if shift.shift=='O':
            print("now date time: %s, %s" % (now_datetime, shift.start_hour.strftime("%Y-%m-%d %H:%M"))  )
            if now_datetime == shift.start_hour.strftime("%Y-%m-%d %H:%M"):
                return True, shift.message
            else:
                return False, ""
        elif shift.shift=='D':
            if now_time == shift.start_hour.strftime("%H:%M"):
                return True, shift.message
            else:
                return False,""
        elif shift.shift=='W':
            if now_time == shift.start_hour.strftime("%H:%M") and now_week in exec_date:
                return True, shift.message
            else:
                return False,""
        elif shift.shift=='M':
            if now_time == shift.start_hour.strftime("%H:%M") and now_day in exec_date:
                return True, shift.message
            else:
                return False,""
        else:
            return False,""
    except Exception as ex:
        print(ex)
        return False,""
register_events(scheduler)
scheduler.start()
