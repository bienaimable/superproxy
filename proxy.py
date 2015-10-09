import os
from libmproxy import controller, proxy
from libmproxy.proxy.server import ProxyServer
import urllib
import database
import uuid
import time

class StickyMaster(controller.Master):
    def __init__(self, server):
        controller.Master.__init__(self, server)

    def run(self):
        try:
            return controller.Master.run(self)
        except KeyboardInterrupt:
            self.shutdown()

    def handle_request(self, flow):
        # Edit the flow here
        flow.reply()

    def handle_response(self, flow):
        add_to_db(flow)
        # Print some stuff to stdout
        print_stdout(flow)
        flow.reply()


def add_to_db(flow):
    port = flow.request.port
    headers = flow.request.headers
    host = flow.request.host
    path = flow.request.path
    content = flow.request.content
    path = flow.request.path
    webrequest = database.WebRequest(
        id=uuid.uuid4().hex,
        timestamp=time.time(),
        host=host,
        path=path,
        content=content
    )
    conversation = database.WebConversation()

def print_stdout(flow):
    port = flow.request.port
    headers = flow.request.headers
    host = flow.request.host
    path = flow.request.path
    content = flow.request.content
    path = flow.request.path
    if "criteo" in flow.request.host:
        print("")
        print("____________________REQUEST___________________")
        try:
            referer = headers['Referer'][0]
        except IndexError:
            referer = None
        print(referer)
        print(host)
        print(path)
        if "?" in path:
            query = path.split("?", 1)[1]
            for keyvalue in query.split("&"):
                key, value = keyvalue.split("=", 1)
                print(urllib.unquote(key) + " : " + urllib.unquote(value))


def run(port):
    config = proxy.ProxyConfig(port=port, cadir=".")
    server = ProxyServer(config)
    m = StickyMaster(server)
    m.run()

if __name__ == '__main__':
    port = 8080
    database.create()
    run_proxy(port)
