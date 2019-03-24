#!/usr/bin/python
# encoding:utf8
from rest_framework import serializers
from . import models


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Schedule
        fields = ('name', 'schedule_operator', 'start_time', "message")
