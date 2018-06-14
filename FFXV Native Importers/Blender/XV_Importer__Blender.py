import bpy
import sys
import math
import time
import struct
import numpy as np
from XV_read import *
import bmesh as bmesh
import mathutils as mu
from XV_meshWhipper import *
from XV_paletteKnife import *
from XV_boneCruncher import *
from rna_prop_ui import rna_idprop_ui_prop_get as prop
from bpy_extras.io_utils import unpack_list, unpack_face_list




from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from numpy.linalg import inv


class ImportSomeData(Operator, ImportHelper):
	"""This appears in the tooltip of the operator and in the generated docs"""
	bl_idname = "import_test.some_data"  # important
	bl_label = "Import Final Fantasy XV Model"

	filename_ext = ".gfxbin"

	filter_glob = StringProperty(
			default="*.gfxbin",
			options={'HIDDEN'},
			)

	use_setting = BoolProperty(
			name="Example Boolean",
			description="Example Tooltip",
			default=True,
			)

	type = EnumProperty(
			name="Example Enum",
			description="Choose between two items",
			items=(('OPT_A', "First Option", "Description one"),
					('OPT_B', "Second Option", "Description two")),
					default='OPT_A',
			)
	
	def execute(self, context):
		closeGPU           = False
		closeAMDL          = False
		BIND               = False
		createSkeleton     = True
		V_28               = True
		
		
		
		
		version = float(bpy.app.version_string[:4])
		if version < 2.8: V_28 = False
		
		gfx_name = self.filepath
		fsize = os.path.getsize(gfx_name)
		path_name = os.path.dirname(gfx_name)
		f_idx = gfx_name.rfind("\\")
		ch_name = gfx_name[f_idx + 1:-7].encode('ascii','ignore')
		gfx = open(gfx_name, 'rb')
		
		gpu_name = path_name + "\\" + gfx_name[f_idx + 1:-11] + "gpubin"
		if os.path.exists(gpu_name):
			gpu = open(gpu_name, "rb")
			closeGPU = True
		
		
		skeleton = bone_cruncher(V_28)
		p0 = os.path.split(path_name)
		p1 = p0[0]
		f_idx = p1.rfind("\\")
		amdl_name = p1 + "\\" + p1[f_idx + 1:] + ".amdl"
		
		
		meshName = gfx_name.split('\\')[-1].split('.')[0][:4]
		t1 = time.time()
		
		
		if V_28:
			stuff = bpy.context.view_layer.objects
		else:
			stuff = bpy.context.scene.objects
		
		for x in stuff:
			if x.type == 'ARMATURE':
				createSkeleton = False
				BIND = True
		
		if os.path.exists(amdl_name):
			amdl = open(amdl_name, "rb")
			closeAMDL = True
			if createSkeleton == True:
				skeleton.make_skeleton(amdl, meshName)
				BIND = True
		
		
		top = rd_top(gfx, fsize)
		
		b0 = paint()
		b0.read(gfx)
		b1 = rd_bones1(gfx)
		
		mesh_count = modelHeader(gfx)
		
		for z in range(mesh_count):
			Mesh = creator(gfx, V_28)
			Mesh.doTheThing(gfx)
			if Mesh.mesh_header.lod_check == 0:
				Mesh.facePuncher(gpu)
				Mesh.FLDSMDFR(gpu)
				if BIND:
					arm = get_arm(V_28)
					skeleton.index_processor(Mesh.weights, Mesh.bone_ids, b0)
					for x in skeleton.wd:
						for p in range(len(skeleton.wd[x]['weights'])):
							vertexWeight = skeleton.wd[x]['weights'][p]
							boneName = skeleton.wd[x]['boneNames'][p]
							vertGroup = Mesh.meshObject.vertex_groups.get(boneName)
							if not vertGroup:
								vertGroup = Mesh.meshObject.vertex_groups.new(boneName)
							vertGroup.add([x], vertexWeight, 'ADD')
					mod = Mesh.meshObject.modifiers.new(type="ARMATURE", name="ArmatureMOD")
					mod.use_vertex_groups = True
					mod.object = arm
		
		
		
		
		elapsed = time.time() - t1
		self.report({'INFO'}, "\n\n" + 'Total Time: ' + str(elapsed) + ' seconds' + "\n\n")
		
		gfx.close()
		if closeGPU:  gpu.close()
		if closeAMDL: amdl.close()
		
		return {'FINISHED'}


def menu_func_import(self, context):
	self.layout.operator(ImportSomeData.bl_idname, text="Text Import Operator")

def register():
	bpy.utils.register_class(ImportSomeData)
	bpy.types.INFO_MT_file_import.append(menu_func_import)

def unregister():
	bpy.utils.unregister_class(ImportSomeData)
	bpy.types.INFO_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
	register()
	bpy.ops.import_test.some_data('INVOKE_DEFAULT')
