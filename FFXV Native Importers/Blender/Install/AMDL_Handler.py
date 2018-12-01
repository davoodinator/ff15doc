from XV_Blender.XV_read import *
import string
import struct
import io


class AMDL_Handler:
	def __init__(self, file_h):
		self.isDuscae = Duscae_manHandler(file_h)
		self.relative_offsets     = [112, 96,80,64,48,32,16]
		if self.isDuscae:
			self.relative_offsets = [128,112,96,80,64,48,32]
		self.juryRig = False
	
	
	def get_stuff(self, file_h):
		file_h.seek(0,0)
		file_size = struct.unpack("<L",file_h.read(4))[0]
		unk = struct.unpack("<L",file_h.read(4))[0]
		block2_offset = struct.unpack("<L",file_h.read(4))[0]
		offset_flag = struct.unpack("<L",file_h.read(4))[0]
		theOffset = self.relative_offsets[offset_flag]
		
		
		if self.isDuscae:
			file_h.seek(840,0)
		else:
			file_h.seek(296,0)
		self.offset_to_end_of_names = struct.unpack("<L",file_h.read(4))[0] + theOffset
		
		file_h.seek(156,1)
		
		
		self.namesStart = struct.unpack("<L",file_h.read(4))[0] + self.relative_offsets[0]
		unk = struct.unpack("<L",file_h.read(4))[0]
		
		self.boneCount = struct.unpack("<H",file_h.read(2))[0]
		file_h.seek(self.namesStart,0)
		
		
		for j in range(self.boneCount):
			bn = readString(file_h)
			if j == 0 and bn != "Trans": self.juryRig = True
			sc = len(bn) + 1
			file_h.seek(48-sc,1)
		
		
		self.trans_header = rd_xfrm_header(file_h, self.isDuscae)
		
		
		
		
		if self.isDuscae == False:
			file_h.seek(self.trans_header["count_0"] *2, 1)    # block 1  uint16
			file_h.seek(self.trans_header["count_0"] *2, 1)    # block 2  uint16
		
		
		if self.isDuscae:
			self.pCount = self.trans_header["parentID_count"]
		else:
			self.pCount = self.trans_header["count_1"]
		
		self.pids_start = file_h.tell()
		for p in range(self.pCount):    # block 3  uint16
			id = struct.unpack("<H",file_h.read(2))[0]
			if id == 65535: continue    # excluded in parentID_count
		
		
		if self.isDuscae == False:
			file_h.seek(self.trans_header["count_1"] *2, 1)    # block 4  uint16
			file_h.seek(self.trans_header["count_1"] *2, 1)    # block 5  uint16
			
			file_h.seek(self.trans_header["count_1"] *4, 1)    # block 6  uint32
			file_h.seek(align(file_h.tell(), 16), 0)
			
			file_h.seek(self.trans_header["count_1"] *16, 1)   # block 7  4x fp32
			file_h.seek(align(file_h.tell(), 16), 0)
			
			file_h.seek(self.trans_header["count_1"] *16, 1)   # block 8  4x fp32
			file_h.seek(align(file_h.tell(), 16), 0)
		else:  # Episode Duscae only has blocks 3-6
			skip = ((self.pCount*2)*2) + (self.pCount*4)
			file_h.seek(skip, 1)
			file_h.seek(align(file_h.tell(), 16), 0)
		
		
		self.transforms_offset = file_h.tell()
