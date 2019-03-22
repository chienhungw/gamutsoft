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


def handle_excel(file_name, flag=1):
    """
    :description 整理Excel表格获取排班信息
    :param file_name:
    :param flag:
    :return:
    """
    bk = xlrd.open_workbook(file_name)
    table = bk.sheet_by_name("Sheet1")
    date_list = table.row_values(0, start_colx=3)
    ncols = table.ncols - 3
    schedule_list = []
    if flag == 0:
        models.Schedule.objects.all().delete()
    print("===========")
    for col in range(ncols):
        user_type = table.col_values(0, start_rowx=2, end_rowx=None)  # 获取用户组信息
        user = table.col_values(1, start_rowx=2, end_rowx=None)  # 获取操作人员信息
        schedule = table.col_values(col + 3, start_rowx=2, end_rowx=None)  # 获取排班信息
        date_now = date(1899, 12, 30) + timedelta(days=int(date_list[col]))
        for idx in range(len(user)):
            if schedule[idx] != "休" and schedule[idx]:
                try:
                    username = models.Operator.objects.get(username=user[idx].strip())
                    if username.team != user_type[idx].strip():
                        username.team = user_type[idx].strip()
                        username.save()
                    schedule_name = models.Shift.objects.get(name=schedule[idx])  # 获取排班信息
                    if username and schedule_name:
                        start, end = getStartAndEnd(date_now, schedule[idx])
                        print("success", user[idx], date_now, schedule[idx], start, end)
                        models.Schedule.objects.create(user=username, schedule_type=schedule_name, start_time=start,
                                                       end_time=end, enabled=1)  # 新增排班信息
                except:
                    print("fail", user[idx], date_now, schedule[idx])

                    pass



def upload_file(request):
    """
    上传文件的request方法
    :param request:
    :return:
    """
    print("upload_file")
    if request.method == 'POST':
        form = forms.UploadExcelForm(request.POST, request.FILES)  # 注意获取数据的方式
        if form.is_valid():
            # filename = str(request.FILES.get("file_path")[""])
            # print(filename)
            for file in os.listdir(MEDIA_ROOT):
                os.remove(os.path.join(MEDIA_ROOT, file))
            form.save()
            flag = form.cleaned_data["flag"]
            handle_excel(os.path.join(MEDIA_ROOT, os.listdir(MEDIA_ROOT)[0]), flag)
            return redirect(reverse_lazy('itsm_route:tasks'))
    else:
        form = forms.UploadExcelForm()
    return render(request, template_name='itsm_route/excel.html', context={'form': form})
