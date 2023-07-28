import serial
import time
import struct 
import serial.tools.list_ports

serial_port = "COM31"

pack_len = 30
pack_head = b'\xAA\xFF\03\00'
cmd_multi = b'\xFD\xFC\xFB\xFA\x02\x00\x90\x00\x04\x03\x02\x01'
cmd_single = b'\xFD\xFC\xFB\xFA\x02\x00\x80\x00\x04\x03\x02\x01'

reply_multi = b'\xFD\xFC\xFB\xFA\x04\x00\x90\x01\x01\x00\x04\x03\x02\x01'
reply_single = b'\xFD\xFC\xFB\xFA\x04\x00\x80\x01\x01\x00\x04\x03\x02\x01'

class Radar(object) :
	def __init__(self,port = 'COM1'):
		self.x = 0
		self.y = 0
		self.speed = 0
		self.serial = serial.Serial(
			port=port,
			baudrate=256000,
			timeout=1)
		self.serial.write(cmd_single)
		
	# 
	def update(self):
		"""\
        更新 x,y 和 speed,
		返回 x,y。单位均为 mm
        """
		self.serial.read_all()
		raw_data = b''
		while(1):
			raw_data = self.serial.read_until(expected= b"\xCC",size = pack_len)
			if len(raw_data) == pack_len and raw_data[:4] == pack_head:
				break
		# print(raw_data)
		raw_data = struct.unpack('<12H',raw_data[4:4+24]) 
		data = []
		for v in raw_data:
			if v >= 32768:
				v = v -32768
			else:
				v = -v
			data.append(v)
		self.x = data[0]
		self.y = data[1]
		self.speed = data[2]
		return self.x,self.y
		#print(data)
#
# # 选择端口
# port_list = list(serial.tools.list_ports.comports())
# print("\nDetected COM ports:")
# for i in range(0, len(port_list)):
# 	print("	[ID:{}] {}".format(i, port_list[i]))
# inputerror = True  # will be turned to False when the input is correct
# selected = input("Please select the port which you want to open, ID:")
# if selected.isdigit():
# 	if int(selected) < len(port_list):
# 		selected_com = port_list[int(selected)]
# 		print("\nOpening: {}\n".format(selected_com))
# 		inputerror = False
# if inputerror:
# 	print("\nInput error! Please only input the ID number in the list above.")
# try:
# 	radar = Radar(selected_com[0])
#
# 	while(1):
# 		radar.update()
# 		print(radar.x,radar.y)
# except serial.SerialException as e:
# 	print("Serial error: ",e)