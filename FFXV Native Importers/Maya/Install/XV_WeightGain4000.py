import maya.OpenMayaAnim as oma
import maya.OpenMaya as om
from XV_MayaJunk import *
import pymel.core as pm
util = om.MScriptUtil()
import maya.mel as mm





def weight_gain_4000(shapeName, boneArray, VertCount, weight_data, mName, grp):
	clusterName = grp + "-" + shapeName + '_' + 'skinCluster'
	pm.skinCluster(boneArray[:], shapeName, sm=1, mi=4, omi=1, n=clusterName)
	
	skin = mm.eval('findRelatedSkinCluster "'+mName+'"')

	sel = om.MSelectionList();
	sel.add(shapeName)
	meshMObject = om.MObject()
	sel.getDependNode(0,meshMObject)

	sel2 = om.MSelectionList();
	sel2.add(skin)
	skinMObject = om.MObject()
	sel2.getDependNode(0,skinMObject)

	FnSkin = oma.MFnSkinCluster(skinMObject)
	dag_path, skinMObject = get_skin_dag_path_and_mobject(FnSkin)
	weights = om.MDoubleArray()
	influence_paths = om.MDagPathArray()
	influence_count = FnSkin.influenceObjects(influence_paths)
	components_per_influence = weights.length() / influence_count

	# influences
	unused_influences = list()
	influences = [influence_paths[inf_count].partialPathName() for inf_count in xrange(influence_paths.length())]


	wSize = VertCount*influence_count
	weights = om.MDoubleArray(wSize,0.0)


	for inf_count in xrange(VertCount):
		L = weight_data[inf_count]['boneNames']
		W = weight_data[inf_count]['weights']
		for count in xrange(len(L)):
			fg = influences.index(L[count])
			#weights.set(W[count], fg + (inf_count * influence_count))  # implicit type conversion: FP64 -> FP32
			idx = fg + (inf_count * influence_count)
			weights[idx] = W[count]                                     # keeps 64-bit precision
			# http://www.polygon.me/2017/08/tip-2-mdoublearray-bug.html


	influence_array = om.MIntArray(influence_count)
	util.createIntArrayFromList(range(influence_count),influence_array)
	
	FnSkin.setWeights(dag_path, skinMObject, influence_array, weights, False)
