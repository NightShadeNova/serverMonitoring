import subprocess, os, socket, requests

instanceName = socket.gethostname()
api_endpoint = "http://127.0.0.1:8000/api/v1/metrics/push/"

def run_script(sh_path):
    try:
        result = subprocess.run(['bash', sh_path], check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Err: ", e.stderr)
        return None

def push_metrics(metrics):
    try:
        response = requests.post(api_endpoint, json=metrics)
        print("Response: ", response.status_code, response.text)
        return response.status_code
    except Exception as e:
        print("Error while pushing metrics: ", e)
        return None

script_path = '/home/nova/Documents/Projects/scripts/'

getcpu = run_script(os.path.join(script_path, 'cpu.sh'))
getdisk= run_script(os.path.join(script_path, 'disk.sh'))
getmemory= run_script(os.path.join(script_path, 'memory.sh'))

if (getcpu and getdisk and getmemory):
    try:
        metrics = {
            'instance_name': instanceName,
            'cpu_usage': float(getcpu.strip()),
            'disk_usage': float(getdisk.strip()),
            'memory_usage': float(getmemory.strip())
        }
        push_metrics(metrics)
    except Exception as e:
        print("Error with scripts' output: ", e)

