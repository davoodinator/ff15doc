import bpy
import sys
import math
from XV_read import align, readString
import struct
import numpy as np
import mathutils as mu
from numpy.linalg import inv
from rna_prop_ui import rna_idprop_ui_prop_get as prop
from bpy_extras.io_utils import unpack_list, unpack_face_list




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
	def __init__(self, version):
		self.wd = {}
		self.bNames = []
		self.Bones = []
		self.relative_offsets = [112,96,80,64,48,32,16]
		self.influence_names = set()
		self.armature_ob = 0
		self.V_28 = version
	
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
	
	
	def make_skeleton(self, file_h, sk_name):
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
		
		
		
		
		armName = sk_name + " Skeleton"
		armature_da = bpy.data.armatures.new(armName)
		armature_da.draw_type = 'WIRE'
		self.armature_ob = bpy.data.objects.new(armName, armature_da)
		
		if self.V_28:
			bpy.context.scene.collection.objects.link(self.armature_ob)
			self.armature_ob.select_set("SELECT")
		else:
			bpy.context.scene.objects.link(self.armature_ob)
			bpy.context.scene.objects.active = self.armature_ob
		
		
		bpy.context.object.show_x_ray = True
		bpy.ops.object.mode_set(mode='EDIT')
		
		
		for x in range(pCount):    # trans_header["xfrm_count"]
			mtx0 = np.fromfile(file_h, dtype = '<f', count = 16).reshape((4,4))
			mtx0[:,[1,2]] = mtx0[:,[2, 1]]
			mtx0[1:3] = np.flipud(mtx0[1:3])
			
			mtx = mtx0.transpose()
			
			boneName = self.bNames[x]
			
			newBone = bpy.context.active_object.data.edit_bones.new(boneName)
			prop(newBone,"ID", create = True)
			newBone["ID"] = x
			if x > 0:
				BNparent = PIDs[x-1]
				parentName = self.bNames[BNparent]
				mm = inv(mtx)
				pt = mu.Vector((mm[0][3], mm[1][3], mm[2][3]))
				newBone.parent = bpy.context.active_object.data.edit_bones[parentName]
				newBone.head = pt
				newBone.tail = pt + mu.Vector((0.001, 0.001, 0.001))
			else:
				BNparent = 0
				newBone.head = mu.Vector((0,0,0))
				newBone.tail = mu.Vector((0,0,0.1))
		bpy.ops.object.mode_set(mode='OBJECT')
