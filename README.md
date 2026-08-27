# server-monitor

Cloud-Native Server Monitoring API with Per-Instance Alerting and Push Model

## How It Works

### Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                     MONITORED SERVERS                        │
│                                                              │
│  setup.sh (infinite loop, every 15s)                         │
│    └── metrics_push.py                                       │
│          ├── scripts/cpu.sh    ── reads /proc/stat           │
│          ├── scripts/memory.sh ── reads /proc/meminfo        │
│          └── scripts/disk.sh   ── reads df --total           │
│                                                              │
│          POST /api/v1/metrics/push/  (Token auth)            │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    DJANGO API SERVER                         │
│                                                              │
│  POST /api/v1/metrics/push/    - stores Record               │
│                                   checks Thresholds          │
│                                   fires Alert + email        │
│                                                              │
│  GET  /api/v1/metrics/latest/  - latest per server           │
│  GET  /api/v1/metrics/timeseries/ - hourly averages          │
│  GET  /api/v1/alerts/active    - last 10 alerts              │
│                                                              │
│  ┌─────────────────────┐     ┌──────────────────────────┐    │
│  │     PostgreSQL      │     │      Gmail SMTP          │    │
│  │  (Records, Alerts,  │     │  (Threshold alerts via   │    │
│  │   Thresholds)       │     │   email)                 │    │
│  └─────────────────────┘     └──────────────────────────┘    │
│                                                              │
│  DASHBOARD (auto-refreshing)                                 │
│    ├── Status cards     ── polls every 10s                   │
│    ├── Historical chart ── refreshes every 5min              │
│    └── Alert feed       ── polls every 20s                   │
└──────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Collect** — Each monitored server runs `setup.sh`, which loops every 15 seconds. Each iteration calls `metrics_push.py`, which runs three Bash scripts that read system metrics directly from `/proc/stat`, `/proc/meminfo`, and `df`.

2. **Push** — `metrics_push.py` assembles the metrics into a JSON payload (tagged with `hostname` as `instance_name`) and POSTs it to the central Django API, authenticated with a token.

3. **Store & Alert** — The API stores the metrics in PostgreSQL. If a `Threshold` exists for that server instance, the API checks CPU/memory/disk against the configured limits. If exceeded, an `Alert` record is created and an email is sent (with a 2-minute cooldown per metric type to prevent flooding).

4. **Visualize** — The dashboard at `/dashboard/` auto-refreshes:
   - Status cards show live metrics (polls `/api/v1/metrics/latest/` every 10s)
   - Historical chart shows hourly averages over 48h (refreshes every 5min)
   - Alert feed shows the 10 most recent alerts (polls every 20s)

### Tech Stack

| Layer              | Technology                       |
| ------------------ | -------------------------------- |
| Backend            | Django 5.2, Django REST Framework|
| Database           | PostgreSQL                       |
| Frontend           | Bootstrap 5.3, Chart.js 4.4      |
| Auth               | DRF Token Authentication         |
| Metrics Collection | Bash scripts + Python pusher     |
| Email Alerts       | Django SMTP (Gmail)              |

### Project Structure

```
server-monitor/
├── metrics_push.py            # Collects metrics, POSTs to API with auth token
├── setup.sh                   # Infinite loop that runs metrics_push.py
├── scripts/
│   ├── cpu.sh                 # Reads CPU usage from /proc/stat
│   ├── disk.sh                # Reads disk usage from df
│   └── memory.sh              # Reads memory usage from /proc/meminfo
├── requirements.txt
├── .env.example               # Template for required environment variables
└── server-monitoring/         # Django project
    ├── manage.py
    ├── monitoring/            # Project config (settings, urls, wsgi)
    │   └── settings.py        # DB, email, REST_FRAMEWORK, security config
    └── monitor_app/           # Main application
        ├── models.py          # Record, Alert, Threshold
        ├── views.py           # API endpoints + dashboard view
        ├── serializers.py     # DRF serializers
        ├── admin.py           # Admin panel configuration
        ├── tests.py           # API and model tests
        ├── migrations/        # Database migrations
        └── templates/
            └── dashboard.html # Auto-refreshing dashboard
```

### Key Concepts

- **Push Model** — Each server pushes its own metrics (vs. a central server pulling/scraping). This is more scalable and works across firewalls.
- **Per-Instance Thresholds** — Each server can have its own CPU/memory/disk limits configured via the Django admin.
- **Alert Deduplication** — The same metric type on the same server won't re-alert within 2 minutes.
- **Token Authentication** — Only servers with a valid API token can push metrics. Dashboard endpoints are public.

## Local Setup

1. Clone Repository
```
git clone https://github.com/NightShadeNova/server-monitor.git
cd server-monitor
```

2. Create and activate virtual environment
```
python3 -m venv server-monitoring/venv
source server-monitoring/venv/bin/activate
```

3. Install Dependencies
```
pip install -r requirements.txt
```

## PostgreSQL Config

1. Create database
```sql
CREATE DATABASE monitoring;
CREATE USER nova WITH PASSWORD 'root';
GRANT ALL PRIVILEGES ON DATABASE monitoring TO nova;
GRANT ALL PRIVILEGES ON SCHEMA public TO nova;
```

2. Set environment variables (or copy `.env.example` to `.env` and fill in values)
```
export DB_NAME='monitoring'
export DB_USER='nova'
export DB_PASSWORD='root'

export DJANGO_SECRET_KEY='<YOUR_RANDOM_SECRET_KEY>'
export EMAIL_HOST_USER='your.monitoring.sender@gmail.com'
export EMAIL_PASSWORD='YOUR_GENERATED_APP_PASSWORD'
export ALERT_RECIPIENT_EMAIL='your.personal.inbox@example.com'
```

3. Run migrations
```
python server-monitoring/manage.py migrate
python server-monitoring/manage.py createsuperuser
```

4. Create API token for metrics push authentication
```
python server-monitoring/manage.py drf_create_token <your-username>
```
This prints a token like `9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`. Add it to your env:
```
export METRICS_API_TOKEN='your-token-here'
```

5. Configure
Start server - `python server-monitoring/manage.py runserver`
Access Admin - http://127.0.0.1:8000/admin/
Find Threshold, click "Add threshold", set server instance to match the hostname returned by `socket.gethostname()` on your monitored machine.

## Final Starting

1. Run the metrics pusher loop (update your project path first in `setup.sh`)
```
nohup ./setup.sh &
```
