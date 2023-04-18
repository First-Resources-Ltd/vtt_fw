# Number of worker processes to spawn
workers = 4

# Number of threads per worker process
threads = 2

# Bind to this address:port
bind = "127.0.0.1:8000"

# Worker class (sync, eventlet, gevent, gthread, tornado)
worker_class = "gevent"

# Maximum number of requests a worker will process before restarting
max_requests = 1000

# Timeout for worker processes to gracefully shutdown
timeout = 300

# Access log file (None for no log)
accesslog = "/var/log/gunicorn/access.log"

# Error log file (None for no log)
errorlog = "/var/log/gunicorn/error.log"

# Log level (debug, info, warning, error, critical)
loglevel = "debug"

# port
port = 8081

# Path to the application WSGI script
# This assumes the app variable is defined in the file `app.py`
# and the WSGI application is named `application`
# You can also specify the module and application name separately
# using the format: module:application
# For example: "myapp.app:myapp"
wsgi_app = "wsgi:server"
