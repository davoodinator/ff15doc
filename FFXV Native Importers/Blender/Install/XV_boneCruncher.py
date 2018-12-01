import bpy
import sys
import math
import struct
import numpy as np
import mathutils as mu
from numpy.linalg import inv
from XV_Blender.XV_read import *
from XV_Blender.AMDL_Handler import *
from rna_prop_ui import rna_idprop_ui_prop_get as prop
from bpy_extras.io_utils import unpack_list, unpack_face_list




class bone_cruncher:
	def __init__(self, version):
		self.wd = {}
		self.bNames = []
		self.Bones = []
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
	
	
	def make_skeleton(self, file_h, grp):
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
		
		
		
		
		armName = grp + "_Armature"
		armature_da = bpy.data.armatures.new(armName)
		if self.V_28:
			armature_da.display_type = 'STICK'
		else:
			armature_da.draw_type = 'WIRE'
		self.armature_ob = bpy.data.objects.new(armName, armature_da)
		self.armature_ob.data.name = grp + "_Armature_Data"
		
		
		
		
		if self.V_28:
			if collectionExists(grp):
				bpy.data.collections[grp].objects.link(self.armature_ob)
			else:
				bpy.context.scene.collection.objects.link(self.armature_ob)
			bpy.context.view_layer.objects.active = self.armature_ob
			self.armature_ob.show_in_front = True
		else:
			bpy.context.scene.objects.link(self.armature_ob)
			bpy.context.scene.objects.active = self.armature_ob
			bpy.context.object.show_x_ray = True
		
		
		bpy.ops.object.mode_set(mode='EDIT')
		
		
		
		for x in range(amdl_data.pCount):
			mtx0 = np.fromfile(file_h, dtype = '<f', count = 16).reshape((4,4))
			if x == 0 and amdl_data.juryRig == True:
				file_h.seek(-64,1)
			
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
