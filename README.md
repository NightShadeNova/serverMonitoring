# server-monitor
Cloud-Native Server Monitoring API with Per-Instance Alerting and Push Model

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

## PostgreSQL config
1. Create database
```sql
CREATE DATABASE monitoring;
CREATE USER nova WITH PASSWORD 'root';
GRANT ALL PRIVILEGES ON DATABASE monitoring TO nova;
-- For PostgreSQL 15+, also run:
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

4. Configure
Start server - `python server-monitoring/manage.py runserver`
Access Admin - http://127.0.0.1:8000/admin/
Find Threshold, click "Add threshold", set server instance to match the hostname returned by `socket.gethostname()` on your monitored machine.

## Final Starting
1. Run the metrics pusher loop (update your project path first in `setup.sh`)
```
nohup ./setup.sh &
```
