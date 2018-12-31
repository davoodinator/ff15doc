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

from LordBusiness import microManager
from XV_WeightGain4000 import *
from XV_boneCruncher import *
from XV_paletteKnife import *
from XV_meshWhipper import *
from XV_read import *

import string
import struct
import time
import sys
import os
import io


gfx_name = cmds.fileDialog2(fm=1, ff='FFXV .gfxbin (*.gfxbin);;')[0]
scene = microManager(gfx_name)
scene.Taco_Tuesday()

t1 = time.time()
top = rd_top(scene.gfx, scene.fsize)

b0  = paint(scene.groupName)
b0.read(scene.gfx)
b1  = rd_bones1(scene.gfx)

mesh_count = modelHeader(scene.gfx)

for z in xrange(mesh_count):
	Mesh = creator(scene.gfx, scene.filename_wo_ext)
	Mesh.doTheThing(scene.gfx)
	if Mesh.mesh_header.lod_check == 0:
		Mesh.facePuncher(scene.gpu)
		Mesh.FLDSMDFR(scene.gpu, scene.groupName)
		
		if scene.BIND == True:
			v_count = Mesh.mesh_header.vertexCount
			scene.skeleton.index_processor(Mesh.weights, Mesh.bone_ids, b0)
			weight_gain_4000(Mesh.shapeName, list(scene.skeleton.influence_names), v_count, scene.skeleton.wd, Mesh.s2, scene.filename_wo_ext)
		

elapsed = time.time() - t1
print "\n\n\n\n"
print 'Imported file in ', elapsed, ' seconds.'

scene.gfx.close()
if scene.closeGPU:  scene.gpu.close()
if scene.closeAMDL: scene.amdl.close()
