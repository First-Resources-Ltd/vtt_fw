import os
# Number of worker processes to spawn
workers = os.environ['WORKERS']

# Number of threads per worker process
threads = os.environ['THREADS']

# Bind to this address:port
bind = bind = f"{os.environ['HOST']}:{os.environ['EXPOSE_PORT']}"

# Worker class (sync, eventlet, gevent, gthread, tornado)
worker_class = os.environ['WORKER_CLASS']

# Timeout for worker processes to gracefully shutdown
timeout = os.environ['TIMEOUT']

# Access log file (None for no log)
accesslog = os.environ['ACCESS_LOG_FILE']

# Error log file (None for no log)
errorlog = os.environ['ERROR_LOG_FILE']

# Maximum number of requests a worker will process before restarting
# max_requests = os.environ['MAX_REQUESTS']

# Log level (debug, info, warning, error, critical)
loglevel = os.environ['LOG_LEVEL']

# port
port = os.environ['PORT']

# Path to the application WSGI script
# This assumes the app variable is defined in the file `app.py`
# and the WSGI application is named `application`
# You can also specify the module and application name separately
# using the format: module:application
# For example: "myapp.app:myapp"
wsgi_app = "wsgi:server"
