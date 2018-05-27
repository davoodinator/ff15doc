import numpy as np
import string
import struct
import os




def readString(file_h):
	aByte=file_h.read(1)
	s=aByte
	while aByte and ord(aByte) != 0:
		aByte=file_h.read(1)
		s+=aByte
	string=s.rstrip("\x00")
	return string




def align(ptr,alignment):
	alignment -= 1
	return (ptr + alignment) & ~(alignment)




def rd(file_h):
	val = 0
	ch = struct.unpack("B",file_h.read(1))[0]
	if ch   == 0xCE:
		val = struct.unpack("<L",file_h.read(4))[0]
	elif ch == 0xCD:
		val = struct.unpack("<H",file_h.read(2))[0]
	elif ch == 0xCC:
		val = struct.unpack("B",file_h.read(1))[0]
	elif ch == 0xCA:
		val = struct.unpack("<f",file_h.read(4))[0]
	elif ch == 0xDE:
		val = struct.unpack("<H",file_h.read(2))[0]
	elif ch == 0xDC:
		val = struct.unpack("<H",file_h.read(2))[0]
	else:
		val = ch
		if (val & 0xF0) >> 4 == 9:
			val &= 0xF
	return val




def get_unknownCount(k):
	val = 0
	if k == 0x91:
		val = 1
	elif k == 0x92:
		val = 4
	elif k == 0x93:
		val = 7
	elif k == 0x94:
		val = 10
	return val

def getByteCount(type):
	bct = 0
	if type == 6:
		bct = 2
	elif type == 8:
		bct = 2
	elif type == 12:
		bct = 1
	elif type == 14:
		bct = 1
	elif type == 16:
		bct = 4
	elif type == 26:
		bct = 2
	return bct




def get_top_count(file_h, f_size):
	unk0 = rd(file_h)
	unk1 = rd(file_h)
	strlen_n = struct.unpack("B",file_h.read(1))[0] - 0xA0
	stop,p = False,0
	while stop == False and file_h.tell() < f_size:
		st = readString(file_h)
		if "asset_uri" in st:
			stop = True
			unk0 = struct.unpack("B",file_h.read(1))[0]
			strlen0 = struct.unpack("B",file_h.read(1))[0]  # asset_uri
			readString(file_h)                              # asset_uri
			strlen1 = struct.unpack("B",file_h.read(1))[0]  # ref
			readString(file_h)                              # ref
			unk1 = struct.unpack("B",file_h.read(1))[0]
			strlen2 = struct.unpack("B",file_h.read(1))[0]  # file
			readString(file_h)                              # file
			
			p = rd(file_h)
	file_h.seek(0,0)
	return p




def rd_top(file_h, f_size):
	lt = []
	t_count = get_top_count(file_h, f_size)
	unk0 = rd(file_h)
	unk1 = rd(file_h)
	for x in range(t_count):
		strlen_n = struct.unpack("B",file_h.read(1))[0] - 0xA0   # & 0x1F
		n = readString(file_h)
		unk2 = struct.unpack("B",file_h.read(1))[0]
		strlen_a = struct.unpack("B",file_h.read(1))[0]
		lt.append({n:readString(file_h)})
		if x == t_count - 1:
			strlen_2 = struct.unpack("B",file_h.read(1))[0] - 0xA0
			ast = readString(file_h)    # asset_uri
			unk3 = struct.unpack("B",file_h.read(1))[0]
			strlen_3 = struct.unpack("B",file_h.read(1))[0]
			lt.append({ast:readString(file_h)})
			strlen_4 = struct.unpack("B",file_h.read(1))[0] - 0xA0
			rf = readString(file_h)     # ref
			unk4 = struct.unpack("B",file_h.read(1))[0]
			strlen_5 = struct.unpack("B",file_h.read(1))[0]
			lt.append({rf:readString(file_h)})
	return lt




def rd_bones1(file_h):
	name_count = rd(file_h)
	for i in xrange(name_count):
		for j in xrange(12): rd(file_h)
		name_size = struct.unpack("B",file_h.read(1))[0] - 0xA0
		bn = readString(file_h)




def modelHeader(file_h):
	file_h.seek(11,1)
	clusterName = readString(file_h)
	count_maybe = struct.unpack("B",file_h.read(1))[0] & 0xF
	name_size = struct.unpack("B",file_h.read(1))[0] - 0xA0
	ClusterName_name = readString(file_h)
	meshCount = rd(file_h)
	return meshCount




def rd_meshBegin(file_h):
	name_size = struct.unpack("B",file_h.read(1))[0] - 0xA0
	mesh_name = readString(file_h)
	file_h.seek(1,1)
	count = rd(file_h)
	for j in range(count):  # cruft
		rd(file_h)
	file_h.seek(94,1)       # more cruft
	return mesh_name




def rd_meshEnd(file_h):
	unk_byte = struct.unpack("B",file_h.read(1))[0]
	maybe_count = struct.unpack("B",file_h.read(1))[0] & 0xF
	
	file_h.seek(46,1)
	lod_0 = rd(file_h)
	lod_1 = rd(file_h)
	lod_2 = rd(file_h)
	
	poo = struct.unpack("H",file_h.read(2))[0]    # 0xC2 / 0xC3
	
	whoCares = rd(file_h)
	count_9 = struct.unpack("B",file_h.read(1))[0]
	count = get_unknownCount(count_9)
	rd(file_h)
	zero = struct.unpack("B",file_h.read(1))[0]  # 0
	for t in range(count):
		rd(file_h)
	C2 = struct.unpack("B",file_h.read(1))[0]    # 0xC2
	rd(file_h)
	C3 = struct.unpack("B",file_h.read(1))[0]    # 0xC3
	rd(file_h)
	unk_byte = struct.unpack("B",file_h.read(1))[0]
	return lod_0




def data_paver(start, end, count, subCount, type, data):
	if type == 6:       # NORMAL FACTORS
		pos = data[:,start:end].ravel().view(dtype = '<H').reshape((count, subCount))  # ?
		positionData = pos.astype(np.float64)
		return positionData
	
	elif type == 8:
		pos = data[:,start:end].ravel().view(dtype = '<H').reshape((count, subCount))
		return pos
	
	elif type == 12:
		pos = data[:,start:end].ravel().view(dtype = 'B').reshape((count, subCount))
		positionData = pos.astype(np.float64)
		positionData /= 255.0
		return positionData
	
	elif type == 14:    # Vectors
		pos = data[:,start:end].ravel().view(dtype = 'b').reshape((count, subCount))
		positionData = pos.astype(np.float64)
		positionData /= 255.0
		return positionData
	
	elif type == 16:
		pos = data[:,start:end].ravel().view(dtype = '<f').reshape((count, subCount))
		positionData = pos.astype(np.float64)
		return positionData
	
	elif type == 26:
		pos = data[:,start:end].ravel().view(dtype = '<f2').reshape((count, subCount))
		positionData = pos.astype(np.float64)
		return positionData
	
	else:
		print "\n\n"
		print "*******************"
		print "unhandled data type"
		print "*******************"
		print "\n"