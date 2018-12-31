import maya.cmds as cmds

import string
import sys
import os
import io

from Vampires_but_also_Ponies import *
from XV_boneCruncher import *




class microManager():
	def __init__(self,da_name):
		self.closeGPU       = False
		self.closeAMDL      = False
		self.BIND           = False
		self.createSkeleton = True
		self.gfxbin = da_name
	def Taco_Tuesday(self):
		self.fsize = os.path.getsize(self.gfxbin)
		path_name = os.path.dirname(self.gfxbin)
		sf = path_name.split("/")
		self.model_baseID = sf[-2].encode('ascii','ignore')
		
		f_idx = self.gfxbin.rfind("/")
		ch_name = self.gfxbin[f_idx + 1:-7].encode('ascii','ignore')
		self.gfx = open(self.gfxbin, "rb")
		self.filename_wo_ext = self.gfxbin.split("/")[-1].split(".")[0].encode('ascii','ignore')
		gpu_name = path_name + "/" + self.gfxbin[f_idx + 1:-11].encode('ascii','ignore') + "gpubin"
		if os.path.exists(gpu_name):
			self.gpu = open(gpu_name, "rb")
			self.closeGPU = True
		
		
		p0 = os.path.split(path_name)
		p1 = p0[0]
		f_idx = p1.rfind("/")
		self.amdl_name = p1 + "/" + p1[f_idx + 1:] + ".amdl"
		
		
		self.groupName = create_topLevel_group_name(self.model_baseID, self.filename_wo_ext)
		
		self.skeleton = bone_cruncher(self.groupName)
		
		
		#self.groupName = self.model_baseID + "__GROUP"
		if cmds.objExists(self.groupName):
			pass
		else:
			cmds.group(em=True, name=self.groupName)
		
		
		
		
		sel = cmds.ls(type = "joint")
		for x in sel:
			if self.groupName in x:
				self.createSkeleton = False
				break
		
		
		
		
		if os.path.exists(self.amdl_name):
			self.BIND = True
			self.amdl = open(self.amdl_name, "rb")
			self.closeAMDL = True
			if self.createSkeleton == True:
				self.skeleton.make_skeleton(self.amdl)
				obj = cmds.ls(sl=True)
				p = cmds.listRelatives(obj, ap=True, f=True)
				q = p[0].split("|")
				sk_root = cmds.select(q[1])
				s1 = cmds.ls(sl=1)
				s2 = s1[0]
				cmds.parent(s2,self.groupName)