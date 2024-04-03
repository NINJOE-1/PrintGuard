import requests
import json

class PrusaLinkWrapper:
    def __init__(self, host: str, api_key: str, port = 80) -> None:
        self.host = host
        self.port = str(port)
        self.api_key = api_key
        self.headers = {'X-Api-Key': api_key}
    
    def getPrinter(self):
        return requests.get('http://' + self.host + ':' + self.port + '/api/printer', headers=self.headers)
    
    def getNozzle(self):
        return getPrinter().json()["telemetry"]["temp-nozzle"]
    
    def getBed(self):
        return getPrinter().json()["telemetry"]["temp-bed"]
    
    def getMaterial(self):
        return getPrinter().json()["telemetry"]["material"]
    
    def getStatus(self):
        return requests.get('http://' + self.host + ':' + self.port + '/api/v1/status', headers=self.headers)
    
    def getProgress(self):
        return getStatus().json()["job"]["progress"]
    
    def getRemaining(self):
        return getStatus().json()["job"]["time_remaining"]
    
    def stopPrint(self):
        data = {'command': 'cancel'}
        response = requests.post('http://' + self.host + ':' + self.port + '/api/job', json=data, headers=self.headers)
        if response.status_code == 204:
            print("Print job stopped successfully.")
        else:
            print("Failed to stop job. Status code: " + str(response.status_code))
            return False
        return True