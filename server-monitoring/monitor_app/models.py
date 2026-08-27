from django.db import models

class Record(models.Model):
    instance_name = models.CharField(max_length=255)
    timing = models.DateTimeField(auto_now_add=True)
    cpu = models.FloatField()
    memory = models.FloatField()
    disk = models.FloatField()

    def __str__(self):
        return f"Server {self.instance_name} metrics at time {self.timing} are - CPU: {self.cpu}, Disk: {self.disk}, Memory: {self.memory}"

class Alert(models.Model):
    server_instance = models.CharField(max_length=255)
    metric_type = models.CharField(max_length=255)
    value = models.FloatField()
    trigger_time = models.DateTimeField(auto_now_add=True)

class Threshold(models.Model):
    server_instance = models.CharField(max_length=255, unique=True)
    cpu_threshold = models.FloatField()
    memory_threshold = models.FloatField()
    disk_threshold = models.FloatField()
    recipients = models.JSONField(default=list)
