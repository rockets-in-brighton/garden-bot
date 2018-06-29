import http.server
import socketserver
import os
import urllib.parse
import cgi

class RobotServerRequestHandler(http.server.BaseHTTPRequestHandler):
 
        def do_GET(self):
            
            # /menu
            # /requestreboot
            # /confirmreboot
            # /requestshutdown
            # /confirmshutdown
            # /uploadform
            # /showlogs
            # /test

            command = self.path.lower().replace('/', '')
            err = True
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write('<html><head><title>Robot Server Request Handler 1.0</title></head><body>'.encode('utf-8'))

            self.wfile.write('<h1>Robot Server Request Handler 1.1</h1>'.encode('utf-8'))

            # http://192.168.0.231:8000/
            # http://192.168.0.231:8000/menu
            if command == '' or command == 'menu':
                menu = open("menu.html", "r")
                menu_markup = menu.read()
                menu.close()
                self.wfile.write(menu_markup.encode('utf-8'))
                err = False

            # http://192.168.0.231:8000/requestreboot
            if command == 'requestreboot':
                self.wfile.write('<b>Click to confirm reboot:</b><br />'.encode('utf-8'))
                self.wfile.write('<a href="/confirmreboot">Confirm</a>'.encode('utf-8'))
                self.wfile.write(' | '.encode('utf-8'))
                self.wfile.write('<a href="/menu">Cancel</a></li>'.encode('utf-8'))
                err = False

            # http://192.168.0.231:8000/confirmreboot
            if command == 'confirmreboot':
                os.system('sudo reboot')
                err = False
                                 
            # http://192.168.0.231:8000/requestshutdown
            if command == 'requestshutdown':
                self.wfile.write('<b>Click to confirm reboot:</b><br />'.encode('utf-8'))
                self.wfile.write('<a href="/confirmshutdown">Confirm</a></li>'.encode('utf-8'))
                self.wfile.write(' | '.encode('utf-8'))
                self.wfile.write('<a href="/menu">Cancel</a></li>'.encode('utf-8'))
                err = False

            # http://192.168.0.231:8000/confirmshutdown
            if command == 'confirmshutdown':
                os.system('sudo shutdown -h now')
                err = False

            # http://192.168.0.231:8000/uploadform
            if command == 'uploadform':
                uploadform = open("uploadform.html", "r")
                uploadform_markup = uploadform.read()
                uploadform.close()
                self.wfile.write(uploadform_markup.encode('utf-8'))
                self.wfile.write('<a href="/menu">Back to the menu</a></li>'.encode('utf-8'))
                err = False

            # http://192.168.0.231:8000/test
            if command == 'test':
                self.wfile.write('Server Response Test'.encode('utf-8'))
                self.wfile.write('<hr />'.encode('utf-8'))
                self.wfile.write('<a href="/menu">Back to the menu</a></li>'.encode('utf-8'))
                err = False

            # http://192.168.0.231:8000/logs
            if command == 'logs':
                files = os.listdir("./logs/")
                for file in files:
                    row = '<a href=showlog?file=' + file + '>' + file + '</a><br />'
                    self.wfile.write(row.encode('utf-8'))
                self.wfile.write('<hr />'.encode('utf-8'))
                self.wfile.write('<a href="/menu">Back to the menu</a></li>'.encode('utf-8'))
                err = False

            # http://192.168.0.231:8000/showlog?file=xyz
            if command[:13] == 'showlog?file=':
                logfile = open('./logs/' + command[13:], "r")
                logfile_raw = logfile.read()
                logfile.close()
                self.wfile.write(logfile_raw.replace("\n", "<br />").encode('utf-8'))
                self.wfile.write('<br />'.encode('utf-8'))
                self.wfile.write('<hr />'.encode('utf-8'))
                self.wfile.write('<a href="/menu">Back to the menu</a></li>'.encode('utf-8'))
                err = False

            # complain about anything else
            if err:
                self.wfile.write('Sorry, I did not understand that command.<br />'.encode('utf-8'))
                self.wfile.write('<a href="/menu">Back to the menu</a></li>'.encode('utf-8'))

            self.wfile.write('</body></html>'.encode('utf-8'))


        def do_POST(self):

            # upload - for now, just echo the contents back to the page

            content_len = int(self.headers['Content-Length'])
            post_body = self.rfile.read(content_len)
            fields = cgi.parse_qs(post_body)


            #print(len(fields))
            #print(fields)

            for key, value in fields.items():
               if key == b'filename':
                  fn = [x.decode('utf-8') for x in value][0]
               if key == b'filecontents':
                  fc = [x.decode('utf-8') for x in value][0]

            #print(fn)
            #print(fc)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            #self.wfile.write('<html><head><title></title></head><body><form><input type="text" value="'.encode('utf-8'))
            #self.wfile.write(fn.encode('utf-8'))
            #self.wfile.write('" /><br />'.encode('utf-8'))
            #self.wfile.write('<textarea cols="50" rows="10">'.encode('utf-8'))
            #self.wfile.write(fc.replace("%0D%0A", "\r\n").encode('utf8'))
            #self.wfile.write('</textarea></form>'.encode('utf-8'))

            f = open('./' + fn, "w")
            f.write(fc)
            f.close()

            self.wfile.write('Saved file'.encode('utf-8'))
            self.wfile.write('<br />'.encode('utf-8'))
            self.wfile.write('<hr />'.encode('utf-8'))
            self.wfile.write('<a href="/menu">Back to the menu</a>'.encode('utf-8'))

            self.wfile.write('</body></html>'.encode('utf-8'))


server = socketserver.TCPServer(("", 8000), RobotServerRequestHandler)

print("Started om port 8000...")
server.serve_forever()
