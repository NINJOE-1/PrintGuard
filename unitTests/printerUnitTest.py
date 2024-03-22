# Library import
import json, requests
from info import printerIP, printerKey
import PrusaLinkWrapper

passed = 0

printer = PrusaLinkWrapper.PrusaLinkWrapper(printerIP, printerKey)

obj = printer.getPrinter()
print(obj.json()["telemetry"]["temp-nozzle"])
if (obj.json()["telemetry"]["temp-nozzle"] != None):
    print("Temperature receive test passed")
    passed += 1
else:
    print("Temperature receive test failed")
if (printer.stopPrint()):
    print("Stopping print test passed")
    passed += 1
else:
    print("Stopping print test failed")
    
print("\nTests passed: " + str(passed) + "/2")