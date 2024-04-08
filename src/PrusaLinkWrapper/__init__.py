import requests
import json

class PrusaLinkWrapper:
    def __init__(self, host: str, api_key: str, port = 80) -> None:
        self.host = host
        self.port = str(port)
        self.api_key = api_key
        self.headers = {'X-Api-Key': api_key}
    
    def getPrinter(self):
        return requests.get('http://'+self.host+':'+self.port+'/api/printer',headers=self.headers)
    
    def getNozzle(self):
        return requests.get('http://'+self.host+':'+self.port+'/api/printer',headers=self.headers).json()["telemetry"]["temp-nozzle"]
    
    def getBed(self):
        return requests.get('http://'+self.host+':'+self.port+'/api/printer',headers=self.headers).json()["telemetry"]["temp-bed"]
    
    def getMaterial(self):
        return requests.get('http://'+self.host+':'+self.port+'/api/printer',headers=self.headers).json()["telemetry"]["material"]
    
    def getSpeed(self):
        return requests.get('http://'+self.host+':'+self.port+'/api/printer',headers=self.headers).json()["telemetry"]["print-speed"]
    
    def getHeight(self):
        return requests.get('http://'+self.host+':'+self.port+'/api/printer',headers=self.headers).json()["telemetry"]["z-height"]
    
    def getPrintingStatus(self):
        return requests.get('http://'+self.host+':'+self.port+'/api/printer',headers=self.headers).json()["state"]["flags"]["printing"]
    
    def getStatus(self):
        return requests.get('http://'+self.host+':'+self.port+'/api/v1/status',headers=self.headers)
    
    def getProgress(self):
        return requests.get('http://'+self.host+':'+self.port+'/api/v1/status',headers=self.headers).json()["job"]["progress"]
    
    def getRemaining(self):
        return requests.get('http://'+self.host+':'+self.port+'/api/v1/status',headers=self.headers).json()["job"]["time_remaining"]
    
    def getPrinting(self):
        return requests.get('http://'+self.host+':'+self.port+'/api/v1/status',headers=self.headers).json()["job"]["time_printing"]
    
    def getState(self):
        return requests.get('http://'+self.host+':'+self.port+'/api/v1/status',headers=self.headers).json()["printer"]["state"]
    
    def getNozzleTarget(self):
        return requests.get('http://'+self.host+':'+self.port+'/api/v1/status',headers=self.headers).json()["printer"]["target_nozzle"]
    
    def getBedTarget(self):
        return requests.get('http://'+self.host+':'+self.port+'/api/v1/status',headers=self.headers).json()["printer"]["target_bed"]
    
    def stopPrint(self):
        data = {'command': 'cancel'}
        response = requests.post('http://' + self.host + ':' + self.port + '/api/job', json=data, headers=self.headers)
        if response.status_code == 204:
            print("Print job stopped successfully.")
        else:
            print("Failed to stop job. Status code: " + str(response.status_code))
            return False
        return True
    
    def pausePrint(self):
        data = {'command': 'pause'}
        response = requests.post('http://' + self.host + ':' + self.port + '/api/job', json=data, headers=self.headers)
        if response.status_code == 204:
            print("Print job stopped successfully.")
        else:
            print("Failed to stop job. Status code: " + str(response.status_code))
            return False
        return True