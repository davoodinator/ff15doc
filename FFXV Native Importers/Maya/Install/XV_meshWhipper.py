import maya.OpenMayaAnim as oma
import maya.api.OpenMaya as om2
from XV_WeightGain4000 import *
from XV_boneCruncher import *
from XV_MayaJunk import *
import maya.OpenMaya as om
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mm
from XV_read import *
import numpy as np
import string
import struct
import os




cat_list = ["BLENDWEIGHT", "BLENDINDICES"]

def cat(d, chk):
	g = sum(chk in p for p in d)
	id = g-1
	first_match = chk + "0"
	last_match = chk + str(id)
	new_sub = d[first_match]["item_subCount"] * g
	new_end = d[last_match]["end"]
	if chk[-1]!= "S":
		new_key = chk + "S"
	else:
		new_key = chk
	a = d[first_match].copy()
	if g > 0:
		for x in d.keys():
			if chk in x:
				del d[x]
		d[new_key] = a
		d[new_key]["item_subCount"] = new_sub
		d[new_key]["end"] = new_end




class header():
	def __init__(self, file_h):
		self.f_readCount  = rd(file_h)
		self.face_type    = struct.unpack("B",file_h.read(1))[0]
		self.faces_offset = rd(file_h)
		self.byteSize     = rd(file_h)
		self.vertexCount  = rd(file_h)
		self.chunk_count  = struct.unpack("B",file_h.read(1))[0] & 0xF
		file_h.seek(2,1)
	def readExtra(self, file_h):
		self.mesh_dataStart = rd(file_h)
		self.mesh_totalByteSize = rd(file_h)
		self.lod_check = rd_meshEnd(file_h)




class m():
	def __init__(self, file_h):
		self.counter = []
		self.data = {}
		self.bc = 0
		self.stride = 0
		self.offset = 0
		self.item_count = 0
	
	def read(self, file_h, first = True):
		start = 0
		end = 0
		if first == True:
			self.stride     = struct.unpack("<H",file_h.read(2))[0]
			self.item_count = struct.unpack("<H",file_h.read(2))[0] & 0xF
		else:
			self.stride = struct.unpack("B",file_h.read(1))[0]
			self.offset = rd(file_h)
			self.item_count = struct.unpack("<H",file_h.read(2))[0] & 0xF
		
		for x in range(self.item_count):
			name_size = struct.unpack("B",file_h.read(1))[0] - 0xA0
			name = readString(file_h)
			self.data[name] = {}
			self.data[name]["d_type"] = struct.unpack("B",file_h.read(1))[0]
			if x < self.item_count - 1:
				end = struct.unpack("B",file_h.read(1))[0]
			else:
				end = self.stride
			self.counter.append(end)
			
			if x == 0:
				self.bc = end
			else:
				start = self.counter[x-1]
				self.bc = end - start
			
			self.data[name]["start"] = start
			self.data[name]["end"] = end
			tbc = getByteCount(self.data[name]["d_type"])
			self.data[name]["item_subCount"] = self.bc / tbc
		if first == True:
			file_h.seek(2,1)








class creator:
	def __init__(self, file_gfx):
		self.bone_ids = 0
		self.weights = 0
		self.VA = 0
		self.NA = 0
		self.uArray0 = om2.MFloatArray()
		self.vArray0 = om2.MFloatArray()
		self.uArray1 = om2.MFloatArray()
		self.vArray1 = om2.MFloatArray()
		self.uArray2 = om2.MFloatArray()
		self.vArray2 = om2.MFloatArray()
		self.uArray3 = om2.MFloatArray()
		self.vArray3 = om2.MFloatArray()
		
		self.name = rd_meshBegin(file_gfx)
		self.mesh_header = header(file_gfx)
	def doTheThing(self, file_gfx):
		self.m0 = m(file_gfx)
		self.m0.read(file_gfx, True)
		
		self.m1 = m(file_gfx)
		self.m1.read(file_gfx, False)
		
		self.mesh_header.readExtra(file_gfx)
	
	
	
	def facePuncher(self, file_gpu):
		file_gpu.seek(self.mesh_header.faces_offset,0)
		
		cn = 0
		if self.mesh_header.face_type == 1:
			cn = self.mesh_header.byteSize/4
			fi = np.fromfile(file_gpu, dtype = '<L', count = cn)
		else: # 0
			cn = self.mesh_header.byteSize/2
			fi = np.fromfile(file_gpu, dtype = '<H', count = cn)
		
		# change winding order so normals are correct
		fi_0 = fi.view().reshape((cn/3, 3))
		fi_1 = np.flip(fi_0,1)    # 0 1 2 --> 2 1 0 etc.
		fi_2 = fi_1.ravel()
		
		self.faces = tuple(fi_2)
		self.pCounts =[3]*(len(self.faces)/3)
		
		
		
	def FLDSMDFR(self, file_gpu):
		file_gpu.seek(self.mesh_header.mesh_dataStart,0)
		self.byte_count = self.mesh_header.vertexCount * self.m0.stride
		ti_0 = np.fromfile(file_gpu, dtype = 'B', count = self.byte_count).reshape((self.mesh_header.vertexCount, self.m0.stride))
		
		
		
		
		for x in cat_list: cat(self.m0.data, x)
		for p in self.m0.data:
			g = self.m0.data[p]
			chunc = data_paver(g["start"], g["end"], self.mesh_header.vertexCount, g["item_subCount"], g["d_type"], ti_0)
			if p == "POSITION0":
				self.VA = om2.MFloatPointArray(chunc.tolist())
			elif p == "BLENDINDICES":
				self.bone_ids = chunc.tolist()
			elif p == "BLENDWEIGHTS":
				self.weights = chunc.tolist()
		
		
		
		
		chunk2_start = self.mesh_header.mesh_dataStart + self.m1.offset
		byteCount2 = self.mesh_header.vertexCount * self.m1.stride
		file_gpu.seek(chunk2_start,0)
		ti_1 = np.fromfile(file_gpu, dtype = 'B', count = byteCount2).reshape((self.mesh_header.vertexCount, self.m1.stride))
		
		for j in self.m1.data:
			z = self.m1.data[j]
			chunc = data_paver(z["start"], z["end"], self.mesh_header.vertexCount, z["item_subCount"], z["d_type"], ti_1)
			if j == "NORMAL0":
				Normal_Array0 = chunc[:,0:3].reshape((self.mesh_header.vertexCount, 3))
				Normal_Array = Normal_Array0.tolist()
			elif j == "TANGENT0":
				pass
			elif j == "TEXCOORD0":
				chunc[:,1:2] *= -1
				chunc[:,1:2] += 1
				uvData0 = chunc.tolist()
				u0 = zip(*uvData0)[0]
				v0 = zip(*uvData0)[1]
				self.uArray0.copy(u0)
				self.vArray0.copy(v0)
			elif j == "TEXCOORD1":
				uvData1 = chunc.tolist()
				u1 = zip(*uvData1)[0]
				v1 = zip(*uvData1)[1]
				self.uArray1.copy(u1)
				self.vArray1.copy(v1)
			elif j == "TEXCOORD2":
				uvData2 = chunc.tolist()
				u2 = zip(*uvData2)[0]
				v2 = zip(*uvData2)[1]
				self.uArray2.copy(u2)
				self.vArray2.copy(v2)
			elif j == "TEXCOORD3":
				uvData3 = chunc.tolist()
				u3 = zip(*uvData3)[0]
				v3 = zip(*uvData3)[1]
				self.uArray3.copy(u3)
				self.vArray3.copy(v3)
			elif j == "NORMAL4FACTORS0":
				pass
			elif j == "NORMAL2FACTORS0":
				pass
		
		
		
		
		mesh = om2.MFnMesh()
		ShapeMesh = cmds.group(em=True)
		parentOwner = get_mobject( ShapeMesh )
		meshMObj = mesh.create(self.VA, self.pCounts, self.faces, uValues = self.uArray0, vValues = self.vArray0, parent = parentOwner)
		
		
		cmds.sets(ShapeMesh, e=True,forceElement='initialShadingGroup')
		
		defaultUVSetName = ''
		defaultUVSetName = mesh.currentUVSetName(-1)
		mesh.setUVs (self.uArray0, self.vArray0, defaultUVSetName )
		mesh.assignUVs ( self.pCounts, self.faces, defaultUVSetName )
		
		if len(self.uArray1) > 1:
			mesh.createUVSet('map2')
			mesh.setUVs (self.uArray1, self.vArray1, 'map2' )
			mesh.assignUVs (self.pCounts, self.faces, 'map2' )
		if len(self.uArray2) > 1:
			mesh.createUVSet('map3')
			mesh.setUVs (self.uArray2, self.vArray2, 'map3' )
			mesh.assignUVs (self.pCounts, self.faces, 'map3' )
		if len(self.uArray3) > 1:
			mesh.createUVSet('map4')
			mesh.setUVs (self.uArray3, self.vArray3, 'map4' )
			mesh.assignUVs (self.pCounts, self.faces, 'map4' )
		
		
		vertexIds = range(self.mesh_header.vertexCount)
		self.NA = om2.MVectorArray(Normal_Array)
		mesh.setVertexNormals(self.NA, vertexIds, space = om2.MSpace.kWorld)
		
		cmds.rename(self.name)
		
		s1 = cmds.ls(sl=1)
		self.s2 = s1[0]
		self.shapeName = self.s2.encode('ascii','ignore')