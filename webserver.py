import multiprocessing
from flask import Flask
import database
import proxy

app = Flask(__name__)

@app.route('/')
def mainpage():
    return 'Hello World!'

if __name__ == '__main__':
    database.create()
    proxy_port = 8080
    proxy.run(proxy_port)
    app.run()
