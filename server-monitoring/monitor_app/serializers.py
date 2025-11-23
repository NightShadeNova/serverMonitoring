from rest_framework import serializers
from .models import Record, Alert

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['instance_name', 'cpu', 'memory', 'disk', 'timing']

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['server_instance', 'metric_type', 'value', 'trigger_time']

class MetricSerializer(serializers.Serializer):
    timestamp =  serializers.DateTimeField()
    cpu_avg = serializers.FloatField()
    mem_avg = serializers.FloatField()
    disk_avg = serializers.FloatField()
