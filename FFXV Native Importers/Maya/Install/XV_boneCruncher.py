import maya.api.OpenMaya as om2
import maya.OpenMaya as om
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mm
from XV_read import *
import string
import struct
import io



def rd_xfrm_header(file_h):
		ab = {}
		ex_st = file_h.tell()
		externalFiles_headerSize = struct.unpack("<L",file_h.read(4))[0]
		file_h.seek(ex_st + externalFiles_headerSize, 0)
		
		ab["count_0"] = struct.unpack("<L",file_h.read(4))[0]
		ab["count_1"] = struct.unpack("<L",file_h.read(4))[0]
		ab["xfrm_count"] = struct.unpack("<H",file_h.read(2))[0]
		ab["parentID_count"] = struct.unpack("<H",file_h.read(2))[0]
		if ab["parentID_count"] == 0: ab["parentID_count"] = ab["xfrm_count"]
		unk_count = struct.unpack("<L",file_h.read(4))[0]
		ab["start_offset"] = file_h.tell()
		return ab

class bone_cruncher:
	def __init__(self):
		self.wd = {}
		self.bNames = []
		self.Bones = []
		self.relative_offsets = [112,96,80,64,48,32,16]
		self.influence_names = set()
	
	
	def index_processor(self, w, idx, p):
		x = -1
		for i in w:
			x += 1
			self.wd[x]={'boneNames':[], 'weights':[]}
			y = -1
			for j in i:
				y += 1
				id = int(idx[x][y])
				if j != 0:
					mrBone = p.ta[id]
					
					self.wd[x]['weights'].append(j)
					self.wd[x]['boneNames'].append(mrBone)
					self.influence_names.add(mrBone)
	
	
	def make_skeleton(self, file_h):
		file_size = struct.unpack("<L",file_h.read(4))[0]
		unk = struct.unpack("<L",file_h.read(4))[0]
		block2_offset = struct.unpack("<L",file_h.read(4))[0]
		offset_flag = struct.unpack("<L",file_h.read(4))[0]
		theOffset = self.relative_offsets[offset_flag]
		
		file_h.seek(296,0)
		self.offset_to_end_of_names = struct.unpack("<L",file_h.read(4))[0] + theOffset
		
		file_h.seek(156,1)
		namesOffset = struct.unpack("<L",file_h.read(4))[0] + 112
		unk = struct.unpack("<L",file_h.read(4))[0]
		boneCount = struct.unpack("<H",file_h.read(2))[0]
		file_h.seek(namesOffset,0)
		
		
		for j in range(boneCount):
			bn = readString(file_h)
			self.bNames.append(bn)
			sc = len(bn) + 1
			file_h.seek(48-sc,1)
		
		trans_header = rd_xfrm_header(file_h)
		file_h.seek(trans_header["count_0"] *2, 1)    # block 1  uint16
		file_h.seek(trans_header["count_0"] *2, 1)    # block 2  uint16
		
		pCount = trans_header["parentID_count"]
		PIDs = []
		for p in range(trans_header["count_1"]):      # block 3  uint16
			id = struct.unpack("<H",file_h.read(2))[0]
			if id == 65535: continue    # excluded in parentID_count
			PIDs.append(id)
		
		file_h.seek(trans_header["count_1"] *2, 1)    # block 4  uint16
		file_h.seek(trans_header["count_1"] *2, 1)    # block 5  uint16
		
		file_h.seek(trans_header["count_1"] *4, 1)    # block 6  uint32
		file_h.seek(align(file_h.tell(), 16), 0)
		
		file_h.seek(trans_header["count_1"] *16, 1)   # block 7  4x fp32
		file_h.seek(align(file_h.tell(), 16), 0)
		
		file_h.seek(trans_header["count_1"] *16, 1)   # block 8  4x fp32
		file_h.seek(align(file_h.tell(), 16), 0)
		
		
		
		
		self.mArray = []
		for x in range(pCount):
			self.mtx = struct.unpack("<16f",file_h.read(64))
			
			
			mm = om2.MMatrix(self.mtx)
			self.mArray.append(mm)
			
			boneName = self.bNames[x]
			
			if x > 0 and x < pCount:
				BNparent = PIDs[x-1]
				mi = mm.inverse()
				mi *= self.mArray[BNparent]
				mm = mi
			else:
				BNparent = 0
			
			mt = om2.MTransformationMatrix(mm)
			
			
			BNps = mt.translation(om2.MSpace.kTransform)
			BNrt = mt.rotation(asQuaternion=True)
			BNrt2 = om.MQuaternion(BNrt[0], BNrt[1], BNrt[2], BNrt[3])
			BNsc = mt.scale(om2.MSpace.kTransform)
			
			
			if x == 0:
				cmds.select(clear=True)
			else:
				pm.select(self.Bones[BNparent])
			
			newBone = pm.joint( p=(0,0,0), name = boneName , radius = 0.1 )
			newBone.setTranslation(BNps)
			newBone.setOrientation(BNrt2)
			newBone.setScale(BNsc)
			
			self.Bones.append(newBone)