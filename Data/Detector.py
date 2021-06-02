# -*- coding: utf-8 -*-
import Utils.DataContainer
import numpy as np
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
from modbus_tk.modbus import ModbusError
import serial
from Utils.EventHook import EventHook


class Detector():
    def __init__(self, name: str,
                 id: int,
                 address: int,
                 countReg: int,
                 unity: str,
                 typeValue: str,
                 timeUpdate: int,
                 baudrate: int = 115200,
                 bytesize: int = 8,
                 parity: str = 'N',
                 stopbits: int = 1,
                 xonxoff: int = 0,
                 rtscts: int = 0,
                 dsrdtr: int = 0,
                 multiplier: float = 1.0,
                 groupe: int = 1) -> None:
        self.id = id
        self.address = address
        self.countReg = countReg
        self.unity = unity
        self.name = name
        self.typeValue = typeValue
        self.groupe = groupe
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.xonxoff = xonxoff
        self.rtscts = rtscts
        self.dsrdtr = dsrdtr
        self.multiplier = multiplier

        self.value = 0
        self.timeUpdate = timeUpdate
        self.lastTimeUpdate = 0
        self.updated = EventHook()
        print('create detector ' + self.name+'\n')

    def readValue(self):
        print('read value '+self.name+'\n')
        port = Utils.DataContainer.instance.currentPort
        self.value = 0
        try:
            # Connect to the slave
            master = modbus_rtu.RtuMaster(serial.Serial(
                port=port,
                baudrate=self.baudrate,
                bytesize=self.bytesize,
                parity=self.parity,
                stopbits=self.stopbits,
                xonxoff=self.xonxoff,
                rtscts=self.rtscts,
                dsrdtr=self.dsrdtr))

            master.set_timeout(0.2)
            result = master.execute(
                self.id, cst.READ_HOLDING_REGISTERS, self.address, self.countReg)
            if(self.typeValue == 'int16'):
                self.value = float(np.int16(result[0]) * self.multiplier)
            if(self.typeValue == 'integer'):
                self.value = float(np.int32(result[0]) * self.multiplier)
            print({'state': True, 'result': result})
            self.updated.fire('{:.2f} {}'.format(
                self.value, self.unity))

            master.close()
        except ModbusError as MdbErr:
            print("%s- Code=%d\n" % (MdbErr, MdbErr.get_exception_code()))

        except modbus_tk.modbus_rtu.ModbusInvalidResponseError as RespErr:
            print("ModbusInvalidResponseError: %s\n" % RespErr)

        except Exception as ex:
            print(ex)
        print('complied read value '+self.name+'\n')

    @staticmethod
    def toJson(o):
        if isinstance(o, Detector):
            return {
                'name': o.name,
                'groupe': o.name,
                'unity': o.unity,
                'typeValue': o.typeValue,
                'timeUpdate': o.timeUpdate,
                'multiplier': o.multiplier,
                'id': o.id,
                'address': o.address,
                'countReg': o.countReg,
                'baudrate': o.baudrate,
                'bytesize': o.bytesize,
                'parity': o.parity,
                'stopbits': o.stopbits,
                'xonxoff': o.xonxoff,
                'rtscts': o.rtscts,
                'dsrdtr': o.dsrdtr,
            }
        return TypeError(f'Object {o} is not of type Detector.')

    @staticmethod
    def fromJson(o):
        return Detector(o['name'],
                        o['id'],
                        o['address'],
                        o['countReg'],
                        o['unity'],
                        o['typeValue'],
                        o['timeUpdate'],
                        o['baudrate'],
                        o['bytesize'],
                        o['parity'],
                        o['stopbits'],
                        o['xonxoff'],
                        o['rtscts'],
                        o['dsrdtr'],
                        o['multiplier'],
                        o['groupe'])
