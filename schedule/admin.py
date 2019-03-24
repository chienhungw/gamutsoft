from django.contrib import admin
from . import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from datetime import date, datetime, timedelta


@admin.register(models.Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'message', 'shift', 'exec_date', 'start_hour', 'enabled')
    list_editable = ('message', 'shift', 'exec_date', 'start_hour', 'enabled',)
    search_fields = ('name',)


class DecadeBornListFilter(admin.SimpleListFilter):
    # 提供一个可读的标题
    title = _('排班日期')
    # 用于URL查询的参数.
    parameter_name = 'date'

    def lookups(self, request, model_admin):
        """
        返回一个二维元组。每个元组的第一个元素是用于URL查询的真实值，
        这个值会被self.value()方法获取，并作为queryset方法的选择条件。
        第二个元素则是可读的显示在admin页面右边侧栏的过滤选项。
        """
        today = datetime.today()
        day_list = [((today + timedelta(days=x)).strftime("%Y%m%d"),
                     _((today - timedelta(days=x)).strftime("%Y-%m-%d"))) for x in
                    range(-5, 10)]
        return day_list

    def queryset(self, request, queryset):
        """
        根据self.value()方法获取的条件值的不同执行具体的查询操作。
        并返回相应的结果。
        """
        today = datetime.today()
        day_list = [(today - timedelta(days=x)).strftime("%Y%m%d") for x in
                    range(-5, 10)]
        if self.value():
            for day in day_list:
                print(day)
                if self.value() == day:
                    filter_day = datetime.strptime(day,"%Y%m%d")
                    return queryset.filter(start_time__gte=filter_day,
                                           start_time__lte=(filter_day + timedelta(days=1)))



@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'operator', 'message', 'start_time', 'enabled')
    list_editable = ('operator', 'message', 'start_time', 'enabled')
    search_fields = ('name', 'operator__name',)
    list_filter = (DecadeBornListFilter,)


@admin.register(models.WorkShift)
class WorkShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_hour', 'start_minute', 'start_message', 'end_hour', 'end_minute', 'end_message',)
    list_editable = ('start_hour', 'start_minute', 'start_message', 'end_hour', 'end_minute', 'end_message',)
    search_fields = ('name',)


@admin.register(models.ScheduleLog)
class ScheduleLogAdmin(admin.ModelAdmin):
    list_display = ('name', 'message', 'start_time', 'result', 'description')
    search_fields = ('name',)


@admin.register(models.Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone',)
    list_editable = ('phone',)
    search_fields = ('name',)
