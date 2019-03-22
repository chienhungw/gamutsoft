from django.contrib import admin
from . import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from datetime import date, datetime, timedelta
@admin.register(models.Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'message','shift','exec_date', 'start_hour', 'enabled')
    list_editable = ('message', 'shift', 'exec_date', 'start_hour', 'enabled',)
    search_fields = ('name',)

@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'message','start_time')
    search_fields = ('name',)

@admin.register(models.WorkShift)
class WorkShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_hour', 'start_minute', 'start_message', 'end_hour', 'end_minute', 'end_message', )
    list_editable = ('start_hour', 'start_minute', 'start_message', 'end_hour', 'end_minute', 'end_message',)
    search_fields = ('name',)

@admin.register(models.ScheduleLog)
class ScheduleLogAdmin(admin.ModelAdmin):
    list_display = ('name', 'message','start_time', 'result', 'description')
    search_fields = ('name',)

@admin.register(models.Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone',)
    list_editable = ('phone',)
    search_fields = ('name',)
