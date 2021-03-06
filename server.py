#!/usr/bin/python
"""
Very simple HTTP server in python.
Usage::
    ./pyserver.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from helperFiles.BlackBox import *

import SocketServer
import signal
import time


class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.kill_now = True
    print "Received Shutdown Signal"

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        
        #Modifications go to command line
        print "Processing Request"

        hdf_name = '.data/latest_profile.h5'
        myBlackBox = IceCube(hdf_name, 1, 10)
        myBlackBox.runAllSteps()
        self.wfile.write('{"array":[1,2,3],"boolean":true,"null":null,"number":123,"object":{"a":"b","c":"d","e":"f"},"string":"Hello From Missoula, Montana"}')

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        print ("in post method")
        self.json_string = self.rfile.read(int(self.headers['Content-Length']))

        self.send_response(200)
        self.end_headers()

        print (self.json_string)

        # Read json_string, to load into variables
        json_data = json.loads(self.json_string)

        # {
        #   "duration": 1000,
        #   "interval": 200,
        #   "map": "velocity",
        #   "ID": 1500
        # }

        print(json_data['duration'])
        print(json_data['interval'])
        print(json_data['map'])
        print(json_data['ID'])

        self.wfile.write("<html><body><h1>POST!</h1></body></html>")


def run(server_class=HTTPServer, handler_class=S, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    # httpd.serve_forever()
    killer = GracefulKiller()
    while True:
        httpd.handle_request()
        if killer.kill_now:
            break
    # requests.get('http://localhost:'+server_address)
    
if __name__ == "__main__":
    from sys import argv
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()


# Credits
# https://gist.github.com/bradmontgomery/2219997
# https://gist.github.com/becxer/30fc93bc56c8ab006a17