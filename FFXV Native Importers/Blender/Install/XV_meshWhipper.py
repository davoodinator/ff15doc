#from XV_WeightGain4000 import *
from XV_Blender.XV_boneCruncher import *
from XV_Blender.XV_read import *
import numpy as np
import string
import struct
import bmesh
import bpy
import os

from bpy_extras.io_utils import unpack_list, unpack_face_list




cat_list = ["BLENDWEIGHT", "BLENDINDICES"]

def cat(d, chk):
	c = {}
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
				c[x] = d[x]
		for i in c.keys():
			del d[i]
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
		#self.chunk_count = rd(file_h)
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
			#self.item_count = rd(file_h)
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
			self.data[name]["item_subCount"] = self.bc // tbc
		if first == True:
			file_h.seek(2,1)




class creator:
	def __init__(self, file_gfx, version, f_name, grp):
		self.meshObject = 0
		self.faces = 0
		self.bone_ids = 0
		self.weights = 0
		self.VA = 0
		self.NA = 0
		self.UVs0 = 0
		self.UVs1 = 0
		self.UVs2 = 0
		self.UVs3 = 0
		
		self.V_28 = version
		
		self.file_name = f_name
		self.name = f_name + "__" + rd_meshBegin(file_gfx)
		self.group_name = grp
		
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
			cn = self.mesh_header.byteSize//4
			fi = np.fromfile(file_gpu, dtype = '<L', count = cn)
		else: # 0
			cn = self.mesh_header.byteSize//2
			fi = np.fromfile(file_gpu, dtype = '<H', count = cn)
		
		fi_0 = fi.view().reshape((cn//3, 3))
		
		
		# change winding order so normals are correct
		# 0 1 2 --> 2 1 0
		if self.V_28:
			fi_1 = np.flip(fi_0,1)
		else:
			fi_1 = np.fliplr(fi_0)
		fi_1[:,[0,1]] = fi_1[:,[1,0]]  # 2 1 0 --> 1 2 0
		fi_2 = fi_1.ravel()
		self.faces = tuple(fi_1)
		
		
	def FLDSMDFR(self, file_gpu):
		file_gpu.seek(self.mesh_header.mesh_dataStart,0)
		self.byte_count = self.mesh_header.vertexCount * self.m0.stride
		ti_0 = np.fromfile(file_gpu, dtype = 'B', count = self.byte_count).reshape((self.mesh_header.vertexCount, self.m0.stride))
		
		for x in cat_list: cat(self.m0.data, x)
		for p in self.m0.data:
			g = self.m0.data[p]
			chunc = data_paver(g["start"], g["end"], self.mesh_header.vertexCount, g["item_subCount"], g["d_type"], ti_0)
			if p == "POSITION0":
				chunc[:,[1,2]] = chunc[:,[2,1]]
				self.VA = chunc.tolist()
			elif p == "BLENDINDICES":
				self.bone_ids = chunc.tolist()
			elif p == "BLENDWEIGHTS":
				self.weights = chunc.tolist()
		
		chunk2_start = self.mesh_header.mesh_dataStart + self.m1.offset
		byteCount2 = self.mesh_header.vertexCount * self.m1.stride
		file_gpu.seek(chunk2_start,0)
		ti_1 = np.fromfile(file_gpu, dtype = 'B', count = byteCount2).reshape((self.mesh_header.vertexCount, self.m1.stride))
		
		uv_count = 0
		for j in self.m1.data:
			z = self.m1.data[j]
			chunc = data_paver(z["start"], z["end"], self.mesh_header.vertexCount, z["item_subCount"], z["d_type"], ti_1)
			if j == "NORMAL0":
				Normal_Array0 = chunc[:,0:3].reshape((self.mesh_header.vertexCount, 3))
				Normal_Array0[:,[1,2]] = Normal_Array0[:,[2,1]]
				Normal_Array = Normal_Array0.tolist()
			elif j == "TANGENT0":
				pass
			elif j == "TEXCOORD0":
				uv_count += 1
				chunc[:,1:2] *= -1
				chunc[:,1:2] += 1
				uvData0 = chunc.tolist()
				self.UVs0 = [mu.Vector(x) for x in uvData0]
			elif j == "TEXCOORD1":
				uv_count += 1
				chunc[:,1:2] *= -1
				chunc[:,1:2] += 1
				uvData1 = chunc.tolist()
				self.UVs1 = [mu.Vector(x) for x in uvData1]
			elif j == "TEXCOORD2":
				uv_count += 1
				chunc[:,1:2] *= -1
				chunc[:,1:2] += 1
				uvData2 = chunc.tolist()
				self.UVs2 = [mu.Vector(x) for x in uvData2]
			elif j == "TEXCOORD3":
				uv_count += 1
				chunc[:,1:2] *= -1
				chunc[:,1:2] += 1
				uvData3 = chunc.tolist()
				self.UVs3 = [mu.Vector(x) for x in uvData3]
			elif j == "NORMAL4FACTORS0":
				pass
			elif j == "NORMAL2FACTORS0":
				pass
		
		
		
		
		#old
		'''
		mesh = bpy.data.meshes.new(self.name)
		mesh.vertices.add(len(self.VA))
		mesh.tessfaces.add(len(self.faces))
		mesh.vertices.foreach_set("co", unpack_list(self.VA))
		mesh.tessfaces.foreach_set("vertices_raw", unpack_face_list(self.faces))
		for g in range(uv_count): mesh.tessface_uv_textures.new()
		me_faces = mesh.tessfaces
		'''
		
		
		mesh = bpy.data.meshes.new(self.name)
		mesh.from_pydata(self.VA, [], self.faces)
		if self.V_28:
			for g in range(uv_count): mesh.uv_layers.new(name = self.name + "_TXUV" + "_0" + str(g))
		else:
			for g in range(uv_count): mesh.uv_textures.new(name = self.name + "_TXUV" + "_0" + str(g))
		
		
		#https://blenderartists.org/t/importing-uv-coordinates/595872/5
		UVS = 0
		for g in range(uv_count):
			if   g == 0: UVS = self.UVs0
			elif g == 1: UVS = self.UVs1
			elif g == 2: UVS = self.UVs2
			elif g == 3: UVS = self.UVs3
			vi_uv = {i: uv for i, uv in enumerate(UVS)}
			per_loop_list = [0.0] * len(mesh.loops)
			for loop in mesh.loops:
				per_loop_list[loop.index] = vi_uv.get(loop.vertex_index)
			per_loop_list = [uv for pair in per_loop_list for uv in pair]
			mesh.uv_layers[g].data.foreach_set("uv", per_loop_list)
		
		
		mesh.validate()
		mesh.update()
		
		self.meshObject = bpy.data.objects.new(self.name, mesh)
		
		
		scn_objs = get_objects(self.V_28)
		if self.V_28:
			if collectionExists(self.file_name):
				bpy.data.collections[self.file_name].objects.link(self.meshObject)
			else:
				newCol = bpy.data.collections.new(self.file_name)
				if collectionExists(self.group_name):
					bpy.data.collections[self.group_name].children.link(newCol)
				else:
					bpy.context.scene.collection.children.link(newCol)
				bpy.data.collections[self.file_name].objects.link(self.meshObject)
		else:
			bpy.context.scene.objects.link(self.meshObject)
			for x in scn_objs:
				if x.type == 'ARMATURE' and self.group_name in x.name:
					self.meshObject.parent = x
					break
			self.meshObject.select = True
		
		mesh.polygons.foreach_set("use_smooth", [True] * len(mesh.polygons))
		bpy.context.scene.update()
