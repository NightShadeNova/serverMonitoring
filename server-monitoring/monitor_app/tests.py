from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import Record, Alert, Threshold


class RecordModelTest(TestCase):
    def test_create_record(self):
        rec = Record.objects.create(
            instance_name="test-server", cpu=50.0, memory=60.0, disk=70.0
        )
        self.assertEqual(rec.instance_name, "test-server")
        self.assertEqual(rec.cpu, 50.0)

    def test_str_representation(self):
        rec = Record.objects.create(
            instance_name="test-server", cpu=50.0, memory=60.0, disk=70.0
        )
        self.assertIn("test-server", str(rec))


class ThresholdModelTest(TestCase):
    def test_create_threshold(self):
        t = Threshold.objects.create(
            server_instance="s1",
            cpu_threshold=80.0,
            memory_threshold=85.0,
            disk_threshold=90.0,
        )
        self.assertEqual(t.cpu_threshold, 80.0)
        self.assertEqual(t.recipients, [])

    def test_recipients(self):
        t = Threshold.objects.create(
            server_instance="s2",
            cpu_threshold=80.0,
            memory_threshold=85.0,
            disk_threshold=90.0,
            recipients=["admin@example.com"],
        )
        self.assertEqual(t.recipients, ["admin@example.com"])


class PushEndpointTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Token.objects.create_user(
            username="testuser", email="test@test.com", password="testpass123"
        )
        self.token = self.user.auth_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_push_valid_metrics(self):
        response = self.client.post(
            "/api/v1/metrics/push/",
            data={
                "instance_name": "test",
                "cpu_usage": 45.0,
                "disk_usage": 60.0,
                "memory_usage": 70.0,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Record.objects.count(), 1)

    def test_push_unauthenticated(self):
        unauth_client = APIClient()
        response = unauth_client.post(
            "/api/v1/metrics/push/",
            data={
                "instance_name": "test",
                "cpu_usage": 45.0,
                "disk_usage": 60.0,
                "memory_usage": 70.0,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_push_missing_field(self):
        response = self.client.post(
            "/api/v1/metrics/push/",
            data={"instance_name": "test"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_get_not_allowed(self):
        response = self.client.get("/api/v1/metrics/push/")
        self.assertEqual(response.status_code, 405)
