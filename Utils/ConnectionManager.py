import json
import socket
from datetime import datetime


class ConnectionManager():
    __ipAdress__: str = ''
    __port__: int = 0
    sock = None
    server_address = 0
    __id__: int
    # __reader__: asyncio.StreamReader
    # __writer__: asyncio.StreamWriter

    def __init__(self, ) -> None:
        print('create ConnectionManager')

    def connect(self, id: int, ipAdress: str, port: int) -> bool:
        if(self.sock == None):
            self.__id__ = id
            self.__ipAdress__ = ipAdress
            self.__port__ = port
            # Create a TCP/IP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect the socket to the port where the server is listening
            self.server_address = (self.__ipAdress__, self.__port__)
            try:
                # self.__reader__, self.__writer__ = await asyncio.open_connection(
                #     self.__ipAdress__, self.__port__)
                self.sock.connect(self.server_address)

                self.send(0, '')

                print('connecting to {} {}\n'.format(
                    self.__ipAdress__, self.__port__))
                return True
            except socket.error as exc:
                print("Caught exception socket.error : {}\n".format(exc))
                return False
        else:
            return True

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
            # self.__writer__.write(json.dumps(package).encode())
            # await self.__writer__.drain()
            mes = json.dumps(package).encode()

            length = len(mes)
            lenBytes = length.to_bytes(4, byteorder="little")
            sendData = lenBytes+mes
            self.sock.sendall(sendData)
            package = ''

            length = int.from_bytes(self.sock.recv(4), byteorder="little")
            b = self.sock.recv(length)
            package = b.decode('utf-8')

            #package = data.decode('utf-8')
            return True
        except socket.error as exc:
            print("Caught exception socket.error : {}\n".format(exc))
            return False


instance = ConnectionManager()
