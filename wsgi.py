import os
from app import server

if __name__ == "__main__":
    server.run(host=os.environ['HOST'], port=os.environ['EXPOSE_PORT'], debug=os.environ['DEBUG'])

