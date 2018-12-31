import numpy as np
import string
import struct
import bpy
import os

V_28 = True
version = float(bpy.app.version_string[:4])
if version < 2.8: V_28 = False


def readString(file_h, count = 200):
	aByte = file_h.read(1)
	s = aByte
	c = 0
	while aByte and ord(aByte) != 0 and c < count:
		aByte = file_h.read(1)
		s += aByte
		c += 1
	return s[:-1].decode('ascii', errors='ignore')




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
	elif type == 13:
		bct = 1
	elif type == 14:
		bct = 1
	elif type == 16:
		bct = 4
	elif type == 26:
		bct = 2
	return bct




def rd_top(file_h, f_size):
	lt = []
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
			lt.append({"asset":readString(file_h)})         # asset_uri
			strlen1 = struct.unpack("B",file_h.read(1))[0]  # ref
			lt.append({"ref":readString(file_h)})           # ref
			unk1 = struct.unpack("B",file_h.read(1))[0]
			strlen2 = struct.unpack("B",file_h.read(1))[0]
			lt.append({"gmdl":readString(file_h)})          # gmdl file
			
			
			t = file_h.tell()
			z0 = struct.unpack("B",file_h.read(1))[0]
			z1 = readString(file_h, 3)
			
			if z1 == "src":
				unk2 = struct.unpack("B",file_h.read(1))[0]
				strlen3 = struct.unpack("B",file_h.read(1))[0]
				lt.append({"src":readString(file_h)})       # gmdl file
				u = file_h.tell()
				p = rd(file_h)
				lt.append({"count":p})
				file_h.seek(u,0)
			else:
				file_h.seek(t,0)
				p = rd(file_h)
				lt.append({"count":p})
				file_h.seek(t,0)
	return lt




def rd_bones1(file_h):
	name_count = rd(file_h)
	for i in range(name_count):
		for j in range(12): rd(file_h)
		name_size = struct.unpack("B",file_h.read(1))[0] - 0xA0
		bn = readString(file_h)




def modelHeader(file_h):
	file_h.seek(11,1)
	base = readString(file_h)       #  Usually Parts_Base
	count_maybe = rd(file_h)
	name_size = struct.unpack("B",file_h.read(1))[0] - 0xA0
	ClusterName = readString(file_h)
	meshCount = rd(file_h)
	return meshCount




def rd_meshBegin(file_h):
	name_size = struct.unpack("B",file_h.read(1))[0] - 0xA0
	mesh_name = readString(file_h)
	file_h.seek(1,1)  # ?
	count = rd(file_h)
	for j in range(count):  # cruft
		rd(file_h)
	
	u0 = struct.unpack("B",file_h.read(1))[0]
	u1 = struct.unpack("B",file_h.read(1))[0] # 0xC2
	for j in range(6):      # more cruft
		rd(file_h)
	unk = struct.unpack("B",file_h.read(1))[0] # 0xC3/03
	
	wb = file_h.tell()
	check = rd(file_h)
	wba = file_h.tell() - wb
	file_h.seek(-wba,1)
	
	if isinstance(check, float):  # more floats
		for j in range(12):       # extra cruft w cheese
			rd(file_h)
		file_h.seek(1,1)
	jk = type(mesh_name)
	return mesh_name




def rd_meshEnd(file_h):
	unk = struct.unpack("B",file_h.read(1))[0]
	if unk != 0: file_h.seek(-1,1)
	
	maybe_count = struct.unpack("B",file_h.read(1))[0]
	# maybe_count = rd(file_h)
	
	file_h.seek(46,1)
	lod_0 = rd(file_h)
	lod_1 = rd(file_h)
	lod_2 = rd(file_h)
	
	poo = struct.unpack("H",file_h.read(2))[0]    # 0xC2 / 0xC3
	
	whoCares = rd(file_h)
	count_9 = struct.unpack("B",file_h.read(1))[0]
	count = get_unknownCount(count_9)
	rd(file_h)
	zero = struct.unpack("B",file_h.read(1))[0]
	for t in range(count):
		rd(file_h)
	
	C2 = struct.unpack("B",file_h.read(1))[0]
	if C2 == 0xC2:
		rd(file_h)
		C3 = struct.unpack("B",file_h.read(1))[0]
		if C3 == 0xC3:
			rd(file_h)
			unk_byte = struct.unpack("B",file_h.read(1))[0]
	else:
		file_h.seek(-1,1)
	return lod_0




def Duscae_manHandler(file_h):
	d = True
	file_h.seek(160,0)
	for x in range(112):
		if struct.unpack("<L",file_h.read(4))[0] != 0:
			d = False
			break
	return d




def rd_xfrm_header(file_h, isDuscae):
	ab = {}
	ex_st = file_h.tell()
	externalFiles_headerSize = struct.unpack("<L",file_h.read(4))[0]
	file_h.seek(ex_st + externalFiles_headerSize, 0)
	
	
	if isDuscae:
		ab["parentID_count"] = struct.unpack("<H",file_h.read(2))[0]
	else:
		ab["count_0"] = struct.unpack("<L",file_h.read(4))[0]
		ab["count_1"] = struct.unpack("<L",file_h.read(4))[0]
		ab["xfrm_count"] = struct.unpack("<H",file_h.read(2))[0]
		ab["parentID_count"] = struct.unpack("<H",file_h.read(2))[0]
		if ab["parentID_count"] == 0: ab["parentID_count"] = ab["xfrm_count"]
		unk_count = struct.unpack("<L",file_h.read(4))[0]
		ab["start_offset"] = file_h.tell()
	return ab




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
	
	elif type == 13:
		pos = data[:,start:end].ravel().view(dtype = 'B').reshape((count, subCount))
		return pos
	
	elif type == 14:    # Vectors
		pos = data[:,start:end].ravel().view(dtype = 'b').reshape((count, subCount))
		positionData = pos.astype(np.float64)
		positionData /= 255.0
		return positionData
	
	elif type == 16:
		pos = data[:,start:end].ravel().view(dtype = '<f').reshape((count, subCount))
		positionData = pos.astype(np.float64)
		return positionData
	
	elif type == 20:    # COLOR
		pos = data[:,start:end].ravel().view(dtype = '<L').reshape((count, subCount))
		return positionData
	
	elif type == 26:
		pos = data[:,start:end].ravel().view(dtype = '<f2').reshape((count, subCount))
		positionData = pos.astype(np.float64)
		return positionData
	
	else:
		print("\n\n")
		print("*******************")
		print("unhandled data type")
		print("*******************")
		print("\n\n")




def collectionExists(c_name):
	for x in bpy.data.collections.items():
		if c_name in x:
			return True
	return False

def get_objects(version):
	V28 = version
	if V28:
		return bpy.context.view_layer.objects
	else:
		return bpy.context.scene.objects

def get_object(objs, _name):
	for j in objs:
		if j.name == _name:
			return j

def check_arm(objs,grp):
	chk = True
	for x in objs:
		if x.type == 'ARMATURE' and grp in x.name:
			chk = False
	return chk

def get_arm(objs, grp):
	for x in objs:
		if x.type == 'ARMATURE' and grp in x.name:
			return x

def rename_arm(objs, grp):
	for x in objs:
		if x.type == 'ARMATURE' and grp in x.name:
			x.name = grp + "_Armature"
			x.data.name = grp + "_Armature_Data"
