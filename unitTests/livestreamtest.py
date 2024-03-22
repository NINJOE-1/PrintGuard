#!/usr/bin/python3

# edited by: Cholen Premjeyanth (added function for taking pictures and opening stream) 

# Mostly copied from https://picamera.readthedocs.io/en/release-1.13/recipes2.html (Lab5) Credit is prrovided.
# Run this script, then point a web browser at http:<this-ip-address>:8000
# Note: needs simplejpeg to be installed (pip3 install simplejpeg).

import io
import os
import logging
import socketserver
import subprocess
from http import server
from threading import Condition
from threading import Timer
from datetime import datetime
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput


PAGE = """\
<html>
<head>
<title>picamera2 MJPEG streaming demo</title>
</head>
<body>
<h1>Picamera2 Live Streaming Demo</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
output = StreamingOutput()
picam2.start_recording(JpegEncoder(), FileOutput(output))

# Added Code

def take_screenshot():
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    directory = '/home/cholenprem/Downloads'
    filename = os.path.join(directory, f'test_{timestamp}.jpg')

    try:
        with open(filename, 'wb') as f:
            picam2.capture_image(output=f) 
        logging.info(f'Screenshot saved: {filename}')
    except Exception as e:
        logging.error(f'Error capturing screenshot: {e}')

    # Schedule the next screenshot to be taken after 10 seconds
    screenshot_timer = Timer(20, take_screenshot)
    screenshot_timer.start()

# Start taking screenshots
take_screenshot()


try:
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)
    # Open web browser to the streaming URL (Added)
    subprocess.Popen(['xdg-open', 'http://192.168.2.45:8000'])
    server.serve_forever()
finally:
    picam2.stop_recording()
