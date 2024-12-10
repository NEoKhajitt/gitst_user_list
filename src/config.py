import os

config = {}

config['service_port'] = int(os.environ.get('SERVICE_PORT', 8080))
