import json
import socket
from datetime import datetime
from Data.Detector import Detector


class ConnectionManager():
    __ipAdress__: str = ''
    __port__: int = 0
    sock = None
    server_address = 0
    __id__: int

    def __init__(self, ) -> None:
        print('create ConnectionManager')

    def connect(self, id: int, ipAdress: str, port: int, detectors: list) -> bool:
        if(self.sock == None):
            self.__id__ = id
            self.__ipAdress__ = ipAdress
            self.__port__ = port
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_address = (self.__ipAdress__, self.__port__)
            try:
                self.sock.connect(self.server_address)
                data = []
                for i in list(range(0, len(detectors))):
                    detector = detectors[i]
                    data.append({
                        'Id': detector.idInSystem,
                        'Type': detector.groupe,
                        'Value': round(detector.value, 2)
                    })
                result = self.send(0, data)
                print('connecting to {} {}\n'.format(
                    self.__ipAdress__, self.__port__))
                return result
            except socket.error as exc:
                print("Caught exception socket.error : {}\n".format(exc))
                return False
        else:
            self.sock = None
            return False

    def send(self, operation: int, data) -> bool:
        try:
            date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            package = {
                'Id': self.__id__,
                'Date':  date,
                'Operation': operation,
                'Error': False,
                'Data': json.dumps(data)
            }
            mes = json.dumps(package).encode()

            length = len(mes)
            lenBytes = length.to_bytes(4, byteorder="little")
            sendData = lenBytes+mes
            self.sock.sendall(sendData)
            package = ''
            if(operation != 4):
                length = int.from_bytes(self.sock.recv(4), byteorder="little")
                b = self.sock.recv(length)
                jsonStr = b.decode('utf-8')
                package = json.loads(jsonStr)

                print(package)

                return package['Error'] == False
            return True
        except socket.error as exc:
            print("Caught exception socket.error : {}\n".format(exc))
            self.sock = None
            return False


instance = ConnectionManager()
