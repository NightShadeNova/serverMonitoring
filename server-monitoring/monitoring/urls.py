"""
URL configuration for monitoring project.
"""
from django.contrib import admin
from django.urls import path
from monitor_app.views import MetricsPush, DashboardView, MetricsFetch, ActiveAlerts, LatestRecordFetch

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/metrics/push/', MetricsPush.as_view(), name="metrics_push"),
    path('dashboard/', DashboardView, name='dashboard'),
    path('api/v1/metrics/timeseries/', MetricsFetch.as_view(), name='metrics-fetch-api'),
    path('api/v1/metrics/latest/', LatestRecordFetch.as_view(), name='latest-record-fetch-api'),
    path('api/v1/alerts/active', ActiveAlerts.as_view(), name='active-alerts-api')
]
