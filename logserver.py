import http.server
import socketserver
import os
import urllib.parse
import cgi

class LogServerRequestHandler(http.server.BaseHTTPRequestHandler):
 
        def do_GET(self):
            
            # /log

            command = self.path.lower().replace('/', '')
            err = True
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # http://192.168.0.231:8000/log?data=xyz
            if command[:9] == 'log?data=':
                data = command[9:]
                f = open('./data.log', "w+")
                f.write(data)
                f.close()
                err = False

server = socketserver.TCPServer(("", 8000), LogServerRequestHandler)

print("Started om port 8000...")
server.serve_forever()
