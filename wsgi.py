import os
from app import server

if __name__ == "__main__":
    server.run(host='0.0.0.0', port=os.environ['EXPOSE_PORT'], debug=True)

