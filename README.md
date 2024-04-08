<img src="PrintGuardLogo.png" alt="Image Description" align="left" width="150" height="auto" style="margin-right: 30px">

# Print Guard: <br> Real-time 3D Printer Monitoring and Management System <!-- omit in toc -->

## SYSC 3010 Computer Systems Development Project <!-- omit in toc -->
### Group L2-G9 Members: <!-- omit in toc -->
Joseph Vretenar<br> Basma Aboushaer<br> Samuel Mauricla<br> Raunak Singh Soi<br> Cholen Premjeyanth

### TA: <!-- omit in toc -->
Ben Earle

# Table of Contents <!-- omit in toc -->
- [Project Overview](#project-overview)
  - [Project Description](#project-description)
  - [Project Structure](#project-structure)
    - [Project tree](#project-tree)
- [Creating your own Print Guard](#creating-your-own-print-guard)
  - [Installation Instructions](#installation-instructions)
    - [Hidden Files](#hidden-files)
  - [Run Instructions](#run-instructions)
  - [Expected Results](#expected-results)


# Project Overview
## Project Description

The Print Guard system will monitor an enclosure for the 3D printer as well as allow for remote control of the 3D printers. This will help to prevent crashes by minimizing changes around the printer. Currently the Print Guard system can control Prusa 3D printers. The system uses two DHT22 sensors to monitor the temperature and humidity both inside and outside of the enclosure. The inner sensor is used to adjust the speed of a 120mm fan so the enclosure can maintain a stable temperature. The system also uses a Raspberry Pi camera to take photos and stream a live feed to the GUI. The GUI will show the user all sensor data including printer data, as well as providing them control over the printer and access to the live feed.

## Project Structure

The Print Guard system is split among two Raspberry Pis and two Arduinos. The first Raspberry Pi is used for communication with the Arduinos, database storage, image capturing, and discord notifications. This Raspberry Pi will run ```RPi-Node1.py``` which can be seen in the ```src``` folder below. The Second Raspberry Pi is responsible for streaming and hosting the website, it will be running both ```RPi-Node2.py``` and ```PrintGuardGUI.py``` located below. One of the Arduinos will be running ```fanDeployment.ino``` and the other will be running ```dhtDeployment.ino``` and they should be wired up to the respective parts.

All test functions can be found in either the [endToEndTests](/endToEndTests/) folder or in the [unitTests](/unitTests/README.md) folder. The end to end tests are used to test the communication protocols between devices, while the unit tests are used for testing the individual hardware and software components of the system.

### Project tree
📦src<br>
 ┣ 📂PrusaLinkWrapper<br>
 ┃ ┣ 📂__pycache__<br>
 ┃ ┗ 📜[```__init__.py```](/src/PrusaLinkWrapper/__init__.py)<br>
 ┣ 📂static<br>
 ┃ ┗ 📜```firebaseConfig.js```<br>
 ┣ 📂templates<br>
 ┃ ┗ 📜[```GUITemplate.html```](/src/templates/GUITemplate.html)<br>
 ┣ 📜[```dhtDeployment.ino```](/src/dhtDeployment.ino)<br>
 ┣ 📜[```fanDeployment.ino```](/src/fanDeployment.ino)<br>
 ┣ 📜```info.py```<br>
 ┣ 📜[```PrintGuardGUI.py```](/src/PrintGuardGUI.py)<br>
 ┣ 📜[```RPi-Node1.py```](/src/RPi-Node1.py)<br>
 ┗ 📜[```RPi-Node2.py```](/src/RPi-Node2.py)<br>

# Creating your own Print Guard
## Installation Instructions

To install the Print Guard system first clone the repository on two Raspberry Pis, this will allow you to run both the Arduino connections as well as run the livestream and GUI. The next thing will be to flash the two Arduinos with their respective code files for the fan and DHT sensors. Once the Arduinos are flashed, the system should be wired up according to the picture and schematic located below. 

If using a Prusa printer (Mk4, Mini, or XL), you need to obtain the IP address located under ```Settings > Network > IPv4 Address``` and save it somewhere, you will also need to obtain the API key located under ```Settings > Network > PrusaLink > Password``` and save it as well. These will be used to setup the printer later on. If not using a Prusa printer, then as of right now printer control will not work, and the printer connect lines should be commented out.

The next part is setting up the firebase for real time database collection. This can be setup through the firebase console, the only change needed is to set the read and write rules to both be true. This is something that can be changed in the future to protect your data.

Finally the discord webhook has to be setup, to do you first need a server to setup the notifications on. On this server go to ```Server settings > Integrations > Webhooks > New Webhook``` you can then change the name and select the channel for that bot to send messages to. The Webhook can be copied here and will need to be saved for later.

### Hidden Files

The file structure located [above](#Project-tree) shows two files that are not on the github page, which are ```info.py``` and ```firebaseConfig.js```, this is because they have data specific to you. These files will have to be created manually, with ```info.py``` on both Raspberry Pis and ```firebaseConfig.js``` on the Raspberry Pi running the GUI. 

```Info.py``` should look like this:
```
printerIP = "PRINTER IPv4 ADDRESS"
printerKey = "PRINTER PASSWORD"
firebaseAPI = "YOUR API KEY"
firebaseAuth = "YOUR_PROJECT_ID.firebaseapp.com"
firebaseURL = "YOUR_DATABASE_URL"
firebaseStorage = "YOUR_PROJECT_ID.appspot.com"
DISCORD_WEBHOOK_URL = "YOUR DISCORD WEBHOOK"
```

```firebaseConfig.js``` should look like this:
```
var firebaseConfig = {
    apiKey: "YOUR API KEY",
    authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
    databaseURL: "YOUR_DATABASE_URL",
    storageBucket: "YOUR_PROJECT_ID.appspot.com"
};
```

## Run Instructions

Once everything is downloaded, flashed, wiredup, and setup. The system can be run. The files can be run in any order but the best way to set it up would be to run:<br>1. ```RPiNode1.py```<br>2. ```RPiNode2.py```<br>3. ```PrintGuardGUI.py```<br>The GUI can be connected to locally on the Raspberry Pi by going to ```http://127.0.0.1:5000``` or remotely by going to ```http://RASPBERRYPI-IP:5000``` where RASPBERRYPI-IP is the ip address of teh Raspberry Pi running the GUI.

## Expected Results

Once everything is running, the first result should be a discord notification informing you that the system is operational. The GUI is expected to show the sensor data for the printer nozzle and bed, the internal temperature and humitdity, the external temperature and humidity, and the fan speed. It should also allow you to view the camera by clicking the camera icon. The default password for admin mode is L2-G9 which can be changed on line 137 in [```GUITemplate.html```](/src/templates/GUITemplate.html). Finally you should be able to stop and pause your print with the buttons on the GUI, this will only work if a print is running.