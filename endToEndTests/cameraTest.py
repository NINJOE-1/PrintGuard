import paramiko
from scp import SCPClient
import smbus
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from time import sleep
from info import server, port, user, password

bus = smbus.SMBus(1)
cameraAddress = 0x0a

def main():
    ssh = createSSHClient(server, port, user, password)
    while 1:
        command = bus.read_byte(cameraAddress)
        if (command == 1):
            camera.start()
            camera.capture_file(image_out_location)
            camera.stop()
            scp = SCPClient(ssh.get_transport())
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        gpio.cleanup()
        sys.exit(0)


def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client