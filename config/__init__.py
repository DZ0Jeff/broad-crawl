from utils import Status_job


is_running_crawler = Status_job()
PROCESS = 1
HOSTS = [
    'http://192.168.15.60:5000'
    # 'http://192.168.15.5:5000'
] # list of vps workers