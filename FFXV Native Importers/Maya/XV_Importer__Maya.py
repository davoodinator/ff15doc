#*************************************
#               WARNING               
#         For External Use Only       
#*************************************

import maya.OpenMayaAnim as oma
import maya.api.OpenMaya as om2
import maya.OpenMaya as om
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mm
import numpy as np
import itertools
from XV_read import *
from XV_meshWhipper import *
from XV_paletteKnife import *
from XV_WeightGain4000 import *
from XV_boneCruncher import *
import string
import struct
import time
import sys
import os
import io




closeGPU           = False
closeAMDL          = False
BIND               = False
createSkeleton     = True
if cmds.objExists("Trans"):
	createSkeleton = False

gfx_name = cmds.fileDialog2(fm=1, ff='FFXV .gfxbin (*.gfxbin);;')[0]
fsize = os.path.getsize(gfx_name)
path_name = os.path.dirname(gfx_name)
f_idx = gfx_name.rfind("/")
ch_name = gfx_name[f_idx + 1:-7].encode('ascii','ignore')
gfx = open(gfx_name, "rb")

gpu_name = path_name + "/" + gfx_name[f_idx + 1:-11].encode('ascii','ignore') + "gpubin"
if os.path.exists(gpu_name):
	gpu = open(gpu_name, "rb")
	closeGPU = True

skeleton = bone_cruncher()
p0 = os.path.split(path_name)
p1 = p0[0]
f_idx = p1.rfind("/")
amdl_name = p1 + "/" + p1[f_idx + 1:] + ".amdl"


if os.path.exists(amdl_name):
	BIND = True
	amdl = open(amdl_name, "rb")
	closeAMDL = True
	if createSkeleton == True: skeleton.make_skeleton(amdl)


top = rd_top(gfx, fsize)
t1 = gfx.tell()

b0 = paint()
b0.read(gfx)
t2 = gfx.tell()


b1 = rd_bones1(gfx)
t3 = gfx.tell()

mesh_count = modelHeader(gfx)
t4 = gfx.tell()

for z in xrange(mesh_count):
	Mesh = creator(gfx)
	Mesh.doTheThing(gfx)
	
	if Mesh.mesh_header.lod_check == 0:
		Mesh.facePuncher(gpu)
		Mesh.FLDSMDFR(gpu)
		
		if BIND == True:
			v_count = Mesh.mesh_header.vertexCount
			skeleton.index_processor(Mesh.weights, Mesh.bone_ids, b0)
			weight_gain_4000(Mesh.shapeName, list(skeleton.influence_names), v_count, skeleton.wd, Mesh.s2)
		


gfx.close()
if closeGPU:  gpu.close()
if closeAMDL: amdl.close()