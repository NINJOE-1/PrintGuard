# Library import
import PrusaLinkPy
import json, requests
from info import printerIP, printerKey
from time import sleep

prusaMk4 = PrusaLinkPy.PrusaLinkPy(printerIP, printerKey)

try:
    while True:
        sensor = prusaMk4.get_printer()
        # Display nozzle temp
        print("Nozzle is at: " + str(sensor.json()["telemetry"]["temp-nozzle"]))
        # Display bed temp
        print("Bed is at: " + str(sensor.json()["telemetry"]["temp-bed"]))
        sleep(5)
# will stop running the script when (ctrl + c) is pressed on keyboard
except KeyboardInterrupt:
    print("\nScript terminated")