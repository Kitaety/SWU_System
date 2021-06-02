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
        ConnectionManager.connect(
            self.__id__, self.__ipAdress__, self.__port__)
        self.__networkThread__.start()

    def setPort(self, port):
        self.currentPort = port
        self.__saveSettings__()

    def dispose(self):
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
                'Temperature', 0, 0, 1, '°С', 'int16', 1000)
            self.detectors.append(detector)
            detector: Detector = Detector(
                'PH Metre', 0, 0, 1, '', 'int16', 2000)
            self.detectors.append(detector)
            detector: Detector = Detector(
                'TDS Metre', 0, 0, 1, '', 'integer', 3000)
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
        print(ConnectionManager)
        while True:
            if(ConnectionManager != None):
                if(ConnectionManager.connect(self.__id__, self.__ipAdress__, self.__port__)):
                    lastUpdateTime = int(time.time()*1000)
                    while True:
                        if(int(time.time()*1000) > lastUpdateTime + self.__intervalSend__):
                            data = []
                            for i in list(range(0, len(self.detectors))):
                                d = self.detectors[i]
                                data.append({
                                    'number': i,
                                    'type': d.groupe,
                                    'value': round(d.value, 2)
                                })
                            if(ConnectionManager.send(3, data)):
                                lastUpdateTime = int(time.time()*1000)
                                print('complete send data\n')
                            else:
                                break

            # try:
            #     sock.connect(server_address)
            #     print('connecting to {}\n'.format(server_address))
            #     sock.sendall(str(self.__id__).encode())
            #     lastUpdateTime = int(time.time()*1000)
            #     while True:
            #         if(int(time.time()*1000) > lastUpdateTime + self.__intervalSend__):
            #             print('send data to server {}:{}\n'.format(
            #                 self.__ipAdress__, self.__port__))
            #             package = {
            #                 'id': self.__id__,
            #                 'date': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            #                 'data': []
            #             }
            #             for i in list(range(0, len(self.detectors))):
            #                 d = self.detectors[i]
            #                 package['data'].append({
            #                     'number': i,
            #                     'type': d.groupe,
            #                     'value': round(d.value, 2)
            #                 })
            #             sock.sendall(json.dumps(package).encode())
            #             lastUpdateTime = int(time.time()*1000)
            #             print('complete send data\n')
            # except socket.error as exc:
            #     print("Caught exception socket.error : {}\n".format(exc))


instance = DataContainer()
