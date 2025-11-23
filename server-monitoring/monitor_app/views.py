from django.shortcuts import render
from .models import Record, Alert, Threshold
from django.views.decorators.csrf import csrf_exempt
import json, datetime
from django.utils import timezone, dateparse
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse
from django.db.models.functions import TruncHour
from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RecordSerializer, AlertSerializer, MetricSerializer

@csrf_exempt
def get_metrics(request):
    if request.method == 'POST':
        try:
            metrics = json.loads(request.body)
            rec = Record.objects.create(
                instance_name = metrics['instance_name'],
                cpu = metrics['cpu_usage'],
                disk = metrics['disk_usage'],
                memory = metrics['memory_usage']
            )
            alerts = []
            try:
                threshold = Threshold.objects.get(server_instance=rec.instance_name)

                if rec.cpu > threshold.cpu_threshold:
                    alerts.append(('cpu', rec.cpu))
                if rec.disk > threshold.disk_threshold:
                    alerts.append(('disk', rec.disk))
                if rec.memory > threshold.memory_threshold:
                    alerts.append(('memory', rec.memory))
                for i in alerts:
                    last_alert = Alert.objects.filter(server_instance=rec.instance_name, metric_type=i[0]).order_by('-trigger_time').first()
                    if (not last_alert) or ((timezone.now() - last_alert.trigger_time) > datetime.timedelta(minutes=2)):
                        Alert.objects.create(
                            server_instance = rec.instance_name,
                            metric_type = i[0],
                            value = i[1]
                            )
                        subject = f"{i[0]} Alert on {rec.instance_name}"
                        message = f"""Alert triggered on {rec.instance_name}
Threshold exceeded by {i[0]}
Value: {i[1]}
Time: {timezone.now()}"""
                        recipient = threshold.recipients if threshold.recipients else [settings.ALERT_RECIPIENT_EMAIL]
                        send_mail(
                            subject,
                            message,
                            settings.EMAIL_HOST_USER,
                            recipient,
                            fail_silently=False)
            except Threshold.DoesNotExist:
                print("Threshold does not exist for the given server instance")

            return JsonResponse({"status": "OK", "id": rec.id}, status=201)


        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
        

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
        
    else:
        return HttpResponseBadRequest("POST method only")

def DashboardView(request):
    server_instances = Record.objects.order_by().values_list('instance_name', flat=True).distinct()
    inst = {'server_instances': server_instances}
    return render(request, 'monitor_app/dashboard.html', inst)

class MetricsFetch(APIView):
    def get(self, request):
        instance_name = request.query_params.get('instance', None)
        startime = timezone.now() - datetime.timedelta(hours=48)
        endtime = timezone.now()
        queryset = Record.objects.filter(timing__range=(startime, endtime))
        if instance_name and instance_name.lower() != 'all':
            queryset = queryset.filter(instance_name=instance_name)
            
        val = ['timestamp']
        
        data = queryset.annotate(timestamp=TruncHour('timing')).values('timestamp').annotate(cpu_avg=Avg('cpu'), mem_avg=Avg('memory'), disk_avg=Avg('disk')).order_by('timestamp')
        serializer = MetricSerializer(data, many=True)
        chart_data = {
            #'labels': [item['timestamp'].strftime('%Y-%m-%d %H:%M') for item in serializer.data],
            'labels': [dateparse.parse_datetime(item['timestamp']).strftime('%Y-%m-%d %H:%M') for item in serializer.data],
            'datasets': [
                {'label': 'CPU Avg', 'data': [item['cpu_avg'] for item in serializer.data]},
                {'label': 'Memory Avg', 'data': [item['mem_avg'] for item in serializer.data]},
                {'label': 'Disk Avg', 'data': [item['disk_avg'] for item in serializer.data]}
            ]
        }
        return Response(chart_data)

class LatestRecordFetch(APIView):
    def get(self, request):
        queryset = Record.objects.order_by('instance_name', '-timing').distinct('instance_name')
        serializer = RecordSerializer(queryset, many=True)
        return Response(serializer.data)

class ActiveAlerts(APIView):
    def get(self, request):
        queryset = Alert.objects.all().order_by('-trigger_time')[:10]
        serializer = AlertSerializer(queryset,many=True)
        return Response(serializer.data)
    

  
