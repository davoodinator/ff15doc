import os
import bpy
import sys
import math
import time
import struct
import numpy as np
import bmesh as bmesh
import mathutils as mu
from XV_Blender.XV_read import *
from XV_Blender.AMDL_Handler import *
from XV_Blender.XV_meshWhipper import *
from XV_Blender.XV_paletteKnife import *
from XV_Blender.XV_boneCruncher import *
from XV_Blender.LordBusiness import microManager
from XV_Blender.Vampires_but_also_Ponies import *

from rna_prop_ui import rna_idprop_ui_prop_get as prop
from bpy_extras.io_utils import unpack_list, unpack_face_list




from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from numpy.linalg import inv


class ImportSomeData(Operator, ImportHelper):
	"""This appears in the tooltip of the operator and in the generated docs"""
	bl_idname = "import_test.some_data"
	bl_label  = "Import Final Fantasy XV Model"
	filename_ext = ".gfxbin"
	
	
	'''
	#https://wiki.blender.org/wiki/Reference/Release_Notes/2.80/Python_API/Addons#Class_Property_Registration
	#disabled for the sake of using 1 importer for both 2.79 and 2.80
	filter_glob: StringProperty(
			default="*.gfxbin",
			options={'HIDDEN'},
			)
	use_setting: BoolProperty(
			name="Example Boolean",
			description="Example Tooltip",
			default=True,
			)
	type: EnumProperty(
			name="Example Enum",
			description="Choose between two items",
			items=(('OPT_A', "First Option", "Description one"),
					('OPT_B', "Second Option", "Description two")),
					default='OPT_A',
			)
	'''
	
	
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
		gfx_name = self.filepath
		scene = microManager(gfx_name)
		scene.Taco_Tuesday()
		
		t1 = time.time()
		top = rd_top(scene.gfx, scene.fsize)
		
		b0 = paint()
		b0.read(scene.gfx)
		b1 = rd_bones1(scene.gfx)
		
		mesh_count = modelHeader(scene.gfx)
		
		for z in range(mesh_count):
			Mesh = creator(scene.gfx, scene.V_28, scene.filename_wo_ext, scene.groupName)
			Mesh.doTheThing(scene.gfx)
			if Mesh.mesh_header.lod_check == 0:
				Mesh.facePuncher(scene.gpu)
				Mesh.FLDSMDFR(scene.gpu)
				if scene.BIND:
					arm = get_arm(scene.scene_objects, scene.groupName)
					scene.skeleton.index_processor(Mesh.weights, Mesh.bone_ids, b0)
					for x in scene.skeleton.wd:
						for p in range(len(scene.skeleton.wd[x]['weights'])):
							vertexWeight = scene.skeleton.wd[x]['weights'][p]
							boneName = scene.skeleton.wd[x]['boneNames'][p]
							vertGroup = Mesh.meshObject.vertex_groups.get(boneName)
							if not vertGroup:
								vertGroup = Mesh.meshObject.vertex_groups.new(name = boneName)
							vertGroup.add([x], vertexWeight, 'ADD')
					mod = Mesh.meshObject.modifiers.new(type="ARMATURE", name="ArmatureMOD")
					mod.use_vertex_groups = True
					mod.object = arm
		
		
		
		
		elapsed = time.time() - t1
		self.report({'INFO'}, "\n\n" + 'Total Time: ' + str(elapsed) + ' seconds' + "\n\n")
		
		scene.gfx.close()
		if scene.closeGPU:  scene.gpu.close()
		if scene.closeAMDL: scene.amdl.close()
		
		return {'FINISHED'}


def register():
	bpy.utils.register_class(ImportSomeData)

def unregister():
	bpy.utils.unregister_class(ImportSomeData)

if __name__ == "__main__":
	register()
	bpy.ops.import_test.some_data('INVOKE_DEFAULT')
