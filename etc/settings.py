from multiprocessing import cpu_count

bind = ['0.0.0.0:8000']
workers = cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
max_requests = 1024
timeout = 60
keepalive = 5
reuse_port = True
capture_output = True
errorlog = "-"
accesslog = "-"
