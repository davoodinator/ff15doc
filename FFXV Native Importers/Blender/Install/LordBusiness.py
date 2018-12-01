import os
import io
import sys
import bpy
import string

from XV_Blender.XV_boneCruncher import *
from XV_Blender.XV_read import *
from XV_Blender.Vampires_but_also_Ponies import *




class microManager():
	def __init__(self,da_name):
		self.closeGPU       = False
		self.closeAMDL      = False
		self.BIND           = False
		self.createSkeleton = True
		self.V_28           = True
		self.gfxbin         = da_name
	def Taco_Tuesday(self):
		self.fsize = os.path.getsize(self.gfxbin)
		path_name = os.path.dirname(self.gfxbin)
		sf = path_name.split("\\")
		self.model_baseID = sf[-2]
		
		version = float(bpy.app.version_string[:4])
		if version < 2.8: self.V_28 = False
		
		
		
		
		f_idx = self.gfxbin.rfind("\\")
		self.gfx = open(self.gfxbin, "rb")
		self.filename_wo_ext = self.gfxbin.split("\\")[-1].split(".")[0]
		gpu_name = path_name + "\\" + self.gfxbin[f_idx + 1:-11] + "gpubin"
		if os.path.exists(gpu_name):
			self.gpu = open(gpu_name, "rb")
			self.closeGPU = True
		
		
		p0 = os.path.split(path_name)
		p1 = p0[0]
		f_idx = p1.rfind("\\")
		self.amdl_name = p1 + "\\" + p1[f_idx + 1:] + ".amdl"
		
		
		self.groupName = create_topLevel_group_name(self.model_baseID, self.filename_wo_ext)
		
		self.skeleton = bone_cruncher(self.V_28)
		
		
		if self.V_28:
			if collectionExists(self.groupName):
				pass
			else:
				self.collect = bpy.data.collections.new(str(self.groupName))
				bpy.context.scene.collection.children.link(self.collect)
		
		
		self.scene_objects = get_objects(V_28)
		self.createSkeleton = check_arm(self.scene_objects, self.groupName)
		
		
		if os.path.exists(self.amdl_name):
			self.BIND = True
			self.amdl = open(self.amdl_name, "rb")
			self.closeAMDL = True
			if self.createSkeleton == True:
				self.skeleton.make_skeleton(self.amdl, self.groupName)