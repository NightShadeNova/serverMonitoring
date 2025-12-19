# serverMonitoring
### Cloud-Native Server Monitoring API with Per-Instance Alerting and Push Model
##### Implements a scalable, secure, and separate server monitoring pipeline using the Push Model (similar to a Prometheus Pushgateway) to collect real time system metrics and trigger immediate email alerts based on custom thresholds

## Local Setup
#### Clone Repository 
git clone https://github.com/NightShadeNova/serverMonitoring.git  
cd serverMonitoring

#### Create and activate virtual environment
python3 -m venv venv  
source venv/bin/activate  

#### Install Dependencies
pip install -r requirements.txt

## PostgreSQL config
#### Create database  

CREATE DATABASE monitoring;  
CREATE USER nova WITH PASSWORD 'root';  
GRANT ALL PRIVILEGES ON DATABASE monitoring TO nova;  

#### Set environment variables

(Must match PostgreSQL setup)  
export DB_NAME='monitoring'  
export DB_USER='nova'  
export DB_PASSWORD='root'  

export DJANGO_SECRET_KEY='<YOUR_RANDOM_SECRET_KEY>'  
export EMAIL_HOST_USER='your.monitoring.sender@gmail.com'  
export EMAIL_PASSWORD='YOUR_GENERATED_APP_PASSWORD'  
export ALERT_RECIPIENT_EMAIL='your.personal.inbox@example.com'

#### Run migrations:
python server-monitoring/manage.py migrate  
python server-monitoring/manage.py createsuperuser

#### Configure
Start server - python server-monitoring/manage.py runserver  
Access Admin - http://127.0.0.1:8000/admin/  
Find server config, click on add server config, set server instance to hostname or wtv your socket.gethostname() returns

## Final Starting
#### Run the metrics pusher loop(update your project path first)  
nohup ./run_metrics_loop.sh &
<img width="1283" height="1358" alt="dashboard" src="https://github.com/user-attachments/assets/3f43c82c-1fdb-4668-8863-756d631d82d5" />
<img width="637" height="314" alt="Screenshot_20251002_005436" src="https://github.com/user-attachments/assets/ffd6b21a-83cd-49ba-ad0b-146f601e14ce" />
