import maya.api.OpenMaya as om2
from AMDL_Handler import *
import maya.OpenMaya as om
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mm
from XV_read import *
import string
import struct
import io




class bone_cruncher:
	def __init__(self):
		self.wd = {}
		self.bNames = []
		self.Bones = []
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
		amdl_data = AMDL_Handler(file_h)
		amdl_data.get_stuff(file_h)
		
		file_h.seek(amdl_data.namesStart,0)
		
		if amdl_data.isDuscae:
			name_count = amdl_data.pCount
		else:
			name_count = amdl_data.boneCount
		
		for j in range(name_count):
			bn = readString(file_h)
			self.bNames.append(bn)
			sc = len(bn) + 1
			file_h.seek(48-sc,1)
		
		
		PIDs = []
		file_h.seek(amdl_data.pids_start,0)
		for p in range(amdl_data.pCount):
			id = struct.unpack("<H",file_h.read(2))[0]
			if id == 65535: continue
			if amdl_data.juryRig:
				if id < (amdl_data.pCount - 1) and p != 0:
					id += 1
			PIDs.append(id)
		
		
		file_h.seek(amdl_data.transforms_offset,0)
		self.mArray = []
		for x in xrange(amdl_data.pCount):
			self.mtx = struct.unpack("<16f",file_h.read(64))
			
			if x == 0 and amdl_data.juryRig == True:
				file_h.seek(-64,1)
			
			mm = om2.MMatrix(self.mtx)
			self.mArray.append(mm)
			
			boneName = self.bNames[x]
			
			if x > 0 and x < amdl_data.pCount:
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