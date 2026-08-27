from django.contrib import admin
from .models import Record, Alert, Threshold


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('instance_name', 'timing', 'cpu', 'memory', 'disk')
    list_filter = ('instance_name',)


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('server_instance', 'metric_type', 'value', 'trigger_time')
    list_filter = ('server_instance', 'metric_type')


@admin.register(Threshold)
class ThresholdAdmin(admin.ModelAdmin):
    list_display = ('server_instance', 'cpu_threshold', 'memory_threshold', 'disk_threshold')
