from XV_read import *
import string
import struct




class paint:
	def __init__(self):
		self.ta = {}
	def read(self, file_h):
		count = struct.unpack("B",file_h.read(1))[0] & 0xF
		d_length = count * 9
		file_h.seek(d_length,1)          # unk
		for x in range(6): rd(file_h)    # 6 floats
		file_h.seek(5,1)                 # unk
		name_count = rd(file_h)
		for g in xrange(name_count):
			name_size = struct.unpack("B",file_h.read(1))[0] - 0xA0
			st = readString(file_h)
			id = rd(file_h)
			if id > 65535:
				id >>= 16
				if id == 65535:
					self.ta[g] = st
				else:
					self.ta[id] = st
			else:
				self.ta[g] = st