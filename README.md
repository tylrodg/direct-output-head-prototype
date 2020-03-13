# Direct Output Head Prototype Data Collection and Retrieval Code
Code for Direct Output Head project (Northwestern's Fall-Winter 2019-20 DSGN 384 Sequence)

## Required softwares
Arduino IDE
Latest version of Python 3

## Arduino setup
Follow instructions at https://learn.adafruit.com/adafruit-feather-m0-adalogger/ from the side menu labeled "Arduino IDE Setup" and "Using with Arduino IDE."

## Install dependencies
```
$ python3 -m pip install -r requirements.txt //Installs required python packages
```

## Collecting data
Use the Arduino IDE to upload the collect script when you want to collect data. The default length of a run is 15 seconds (shown at line 62 in collect.ino)
Each time the device is powered on, data collection begins. Please allow a few extra seconds after the 15 second run to turn off the device.

## Retrieving data
Use the Arduino IDE to upload the pull script when you want to retrieve the data files from the headform. After uploading the script, make note of the port number located in the bottom right-hand corner of the IDE, exit the IDE, leave the head plugged into the computer, and run the python script entitled "pull.py" from your command line like so:
```
$ python3 pull.py
```
The will ask a few questions before retrieving the files.
