from Utils.RepeatedTimer import RepeatedTimer
from Utils.Serial import getPorts
from typing import List
from Data.Detector import Detector
import os
import json
import time
from datetime import datetime
import threading
from Utils.ConnectionManager import instance as ConnectionManager


class DataContainer():
    detectors: List[Detector] = list()
    currentPort = ''
    networkState = 'Offline'
    __id__ = 0
    __currentPath__ = ''
    __detectorsFile__ = ''
    __settingsFile__ = ''
    __timeUpdate__ = 1000
    __timer__ = 0
    __ipAdress__ = '127.0.0.1'
    __port__ = 8888
    __intervalSend__ = 30
    __socket__ = 0
    __isUpdatedDetectors__ = False
    __networkThread__ = 0

    def loadData(self):
        self.__loadSettings__()
        self.__loadDetectors__()
        self.__timer__ = RepeatedTimer(
            self.__timeUpdate__/1000, lambda: self.__updateDetectors__())
        self.__networkThread__ = threading.Thread(
            target=self.__sendData__, daemon=True)
        self.__networkThread__.start()

    def setPort(self, port):
        self.currentPort = port
        self.__saveSettings__()

    def dispose(self):
        ConnectionManager.send(4, '')
        self.__timer__.stop()

    def __loadDetectors__(self):
        if(os.path.exists(self.__detectorsFile__)):
            print('Read file detectors.json\n')
            f = open(self.__detectorsFile__, 'r')
            detectors = json.loads(f.read())
            for dict in detectors:
                self.detectors.append(
                    Detector.fromJson(dict))
        else:
            print('Create new file detectors.json\n')
            f = open(self.__detectorsFile__, 'w')
            detector: Detector = Detector(
                1, 'Temperature', 0, 0, 1, '°С', 'int16', 1000)
            self.detectors.append(detector)
            detector: Detector = Detector(
                2, 'PH Metre', 0, 0, 1, '', 'int16', 2000)
            self.detectors.append(detector)
            detector: Detector = Detector(
                3, 'TDS Metre', 0, 0, 1, '', 'integer', 3000)
            self.detectors.append(detector)
            json.dump(self.detectors, f,
                      default=Detector.toJson, indent=4)

    def __loadSettings__(self):
        if(os.path.exists(self.__settingsFile__)):
            print('Read file settings.json\n')
            f = open(self.__settingsFile__, 'r')
            settings = json.loads(f.read())
            self.__id__ = settings['id']
            self.currentPort = settings['com']
            self.__timeUpdate__ = settings['timeUpdate']
            self.__ipAdress__ = settings['ip']
            self.__port__ = settings['port']
            self.__intervalSend__ = settings['timeSend']
        else:
            print('Create new file settings.json\n')
            self.currentPort = getPorts()[0]
            self.__saveSettings__()

    def __saveSettings__(self):
        f = open(self.__settingsFile__, 'w')
        settings = {
            'id': self.__id__,
            'com': self.currentPort,
            'timeUpdate': self.__timeUpdate__,
            'ip': self.__ipAdress__,
            'port': self.__port__,
            'timeSend': self.__intervalSend__
        }
        json.dump(settings, f, indent=4)

    def __updateDetectors__(self):
        if(self.__isUpdatedDetectors__ == False):
            print('update detectors\n')
            self.__isUpdatedDetectors__ = True
            curTime = int(time.time()*1000)
            for detector in self.detectors:
                if(curTime > detector.lastTimeUpdate + detector.timeUpdate):
                    detector.readValue()
                    detector.lastTimeUpdate = curTime
            self.__isUpdatedDetectors__ = False

    def __sendData__(self):
        lastUpdateTime = 0
        while True:
            if(int(time.time()*1000) > lastUpdateTime + self.__intervalSend__):
                if(ConnectionManager.connect(self.__id__, self.__ipAdress__, self.__port__, self.detectors)):
                    self.networkState = 'Online'
                    while True:
                        if(int(time.time()*1000) > lastUpdateTime + self.__intervalSend__):
                            data = []
                            for i in list(range(0, len(self.detectors))):
                                d = self.detectors[i]
                                data.append({
                                    'Id': d.idInSystem,
                                    'Type': d.groupe,
                                    'Value': round(d.value, 2)
                                })
                            if(ConnectionManager.send(3, data)):
                                print('complete send data\n')
                                lastUpdateTime = int(time.time()*1000)
                            else:
                                break
                else:
                    self.networkState = 'Offline'
                    print('not connect')
                    lastUpdateTime = int(time.time()*1000)


instance = DataContainer()
