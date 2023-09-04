#Wrapper for BYD B-Box HVM/HVS/LVS
import socket
import logging
import time

BUFFER_SIZE = 1024
MESSAGE_0 = "010300000066c5e0" #read serial
MESSAGE_1 = "01030500001984cc" #read data
MESSAGE_2 = "010300100003040e"
MESSAGE_3 = "0110055000020400018100f853" #3 start measuring
MESSAGE_4 = "010305510001d517"
MESSAGE_5 = "01030558004104e5"
MESSAGE_6 = "01030558004104e5"
MESSAGE_7 = "01030558004104e5"
MESSAGE_8 = "01030558004104e5"
#// to read the 5th module, the box must first be reconfigured
MESSAGE_9 = "01100100000306444542554700176f" #//9 switch to second turn for the last few cells
MESSAGE_10 = "0110055000020400018100f853" # //10 start measuring remaining cells (like 3)
MESSAGE_11 = "010305510001d517" # //11 (like 4)
MESSAGE_12 = "01030558004104e5" #//12 (like 5)
MESSAGE_13 = "01030558004104e5" #//13 (like 6)


class byd (object):
    def __init__(
        self,
        byd_host = "192.168.16.254",
        byd_port = 8080
    ):
    
        self._byd_host = byd_host
        if (type(byd_port) == str):
            byd_port = int(byd_port)
        self._byd_port = byd_port
        self._bydvalues = []

    def buf2int16SI(self, byteArray, pos): #signed
        result = byteArray[pos] * 256 + byteArray[pos + 1]
        if (result > 32768):
            result -= 65536
        return result

    def buf2int16US(self, byteArray, pos): #unsigned
        result = byteArray[pos] * 256 + byteArray[pos + 1]
        return result

    def read_data(self):  
        try:            
            #connection BYD
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.setblocking(True)
            client.connect((self._byd_host, self._byd_port))

            #message 0
            client.send(bytes.fromhex(MESSAGE_0))

            #read serial
            data = client.recv(BUFFER_SIZE)

            #print(data.hex())
            self.hvs_serial = ""
            for i in range(3, 22):
                self.hvs_serial += chr(data[i])

            self.hvs_batt_type_from_serial = ""
            if data[5] == 51:
                self.hvs_batt_type_from_serial = "HVS"
            if data[5] == 50:
                self.hvs_batt_type_from_serial = "LVS"
            if data[5] == 49:
                self.hvs_batt_type_from_serial = "LVS"
            
            self.hvs_bmu_a = f"V{data[27]}.{data[28]}"
            self.hvs_bmu_b = f"V{data[29]}.{data[30]}"

            if data[33] == 0:
                self.hvs_bmu = self.hvs_bmu_a + "-A"
            else:
                self.hvs_bmu = self.hvs_bmu_b + "-B"
            
            self.hvs_bms = f"V{data[31]}.{data[32]}-{chr(data[34] + 65)}"

            self.hvs_modules = int((data[36] - 16))

            if data[38] == 1:
                self.hvs_grid = "OnGrid"
            else:
                self.hvs_grid = "OffGrid"

            #message 1
            client.send(bytes.fromhex(MESSAGE_1))

            #read data
            data = client.recv(BUFFER_SIZE)
            #print (data.hex())
            self.soc = self.buf2int16SI(data, 3)
            #print ("soc: "+str(self.soc))
            self.maxvolt =self.buf2int16SI(data, 5) * 1.0 / 100.0
            #print ("maxvolt: "+str(self.maxvolt))
            self.minvolt = self.buf2int16SI(data, 7) * 1.0 / 100.0
            #print ("minvolt: "+str(self.minvolt))
            self.soh = self.buf2int16SI(data, 9)
            #print ("soh: "+str(self.soh))
            self.ampere = self.buf2int16SI(data, 11) * 1.0 / 10.0
            #print ("ampere: "+str(self.ampere))
            self.battvolt = self.buf2int16US(data, 13) * 1.0 / 100.0
            #print ("battvolt: "+str(self.battvolt))
            self.maxtemp = self.buf2int16SI(data, 15)
            #print ("maxtemp: "+str(self.maxtemp))
            self.mintemp = self.buf2int16SI(data, 17)
            #print ("mintemp: "+str(self.mintemp))
            self.battemp = self.buf2int16SI(data, 19)
            #print ("battemp: "+str(self.battemp))
            self.error = self.buf2int16SI(data, 29)
            #print ("error: "+str(self.error))
            self.paramt = chr(data[31]) + "." + chr(data[32])
            #print ("paramt: "+str(self.paramt))
            self.outvolt = self.buf2int16US(data, 35) * 1.0 / 100.0
            #print ("outvolt: "+str(self.outvolt))
            self.power = round((self.ampere * self.outvolt) * 100 / 100, 2)
            #print ("power: "+str(self.power))
            self.diffvolt = round((self.maxvolt - self.minvolt) * 100 / 100, 2)
            #print ("diffvolt: "+str(self.diffvolt))

            #message 2
            client.send(bytes.fromhex(MESSAGE_2))

            #read data
            data = client.recv(BUFFER_SIZE)

            self.hvs_batt_type = data[5]
            self.hvs_inv_type = data[3]
            self.hvs_num_cells = 0
            self.hvs_num_temps = 0

            if self.hvs_batt_type == 0:
                pass  # Default case, do nothing
            elif self.hvs_batt_type == 1:
                self.hvs_num_cells = self.hvs_modules * 16
                self.hvs_num_temps = self.hvs_modules * 8
            elif self.hvs_batt_type == 2:
                self.hvs_num_cells = self.hvs_modules * 32
                self.hvs_num_temps = self.hvs_modules * 12
            
            if self.hvs_batt_type_from_serial == "LVS":
                self.hvs_batt_type = "LVS"
                self.hvs_num_cells = self.hvs_modules * 7
                self.hvs_num_temps = 0
            
            if self.hvs_num_cells > 160:
                self.hvs_num_cells = 160
            
            if self.hvs_num_temps > 64:
                self.hvs_num_temps = 64
            
            #message 3 -start messauring
            client.send(bytes.fromhex(MESSAGE_3))
            data = client.recv(BUFFER_SIZE)
            #print(data.hex())

            time.sleep(5)
            client.send(bytes.fromhex(MESSAGE_4))
            #message 5
            client.send(bytes.fromhex(MESSAGE_5))
            data = client.recv(BUFFER_SIZE)
            #print(data.hex())
            #message 5
            client.send(bytes.fromhex(MESSAGE_5))

            data = client.recv(BUFFER_SIZE)
            #print (data.hex())
            self.hvsMaxmVolt = self.buf2int16SI(data, 5)
            self.hvsMinmVolt = self.buf2int16SI(data, 7)
            self.hvsMaxmVoltCell = data[9]
            self.hvsMinmVoltCell = data[10]
            self.hvsMaxTempCell = data[15]
            self.hvsMinTempCell = data[16]
            self.hvsSOCDiagnosis = self.buf2int16SI(data, 53)/10

            MaxCells = 16
            self.hvs_battery_volts_per_cell = {}

            for i in range(MaxCells):
                cell_number = i + 1
                #print (data[i*2+101])
                voltage = self.buf2int16SI(data, i * 2 + 101)
                self.hvs_battery_volts_per_cell[cell_number] = voltage

            #message 5
            client.send(bytes.fromhex(MESSAGE_5))

            #read data
            data = client.recv(BUFFER_SIZE)
            #print (data.hex())

            MaxCells = self.hvs_num_cells - 16
            if MaxCells > 64:
                MaxCells = 64

            for i in range(MaxCells):
                cell_number = i + 1
                voltage = self.buf2int16SI(data, i * 2 + 5)
                self.hvs_battery_volts_per_cell[cell_number] = voltage

            client.send(bytes.fromhex(MESSAGE_5))

            #read data
            data = client.recv(BUFFER_SIZE)
            #print (data.hex())
            MaxCells = self.hvs_num_cells - 80 
            if MaxCells > 48:
                MaxCells = 48

            for i in range(MaxCells):
                cell_number = i + 1
                voltage = self.buf2int16SI(data, i * 2 + 5)
                self.hvs_battery_volts_per_cell[cell_number] = voltage

            self.hvs_battery_temps_per_cell = {}

            MaxTemps = self.hvs_num_temps - 0
            if MaxTemps > 30:
                MaxTemps = 30

            for i in range(MaxTemps):
                temp_cell_number = i + 1
                temp = data[i+103]
                self.hvs_battery_temps_per_cell[temp_cell_number] = temp
            
        except Exception as ex:
            trace = []
            tb = ex.__traceback__
            while tb is not None:
                trace.append(
                    {
                        "filename": tb.tb_frame.f_code.co_filename,
                        "name": tb.tb_frame.f_code.co_name,
                        "lineno": tb.tb_lineno,
                    }
                )
                tb = tb.tb_next
            print(str({"type": type(ex).__name__, "message": str(ex), "trace": trace}))
        finally:
            client.close()