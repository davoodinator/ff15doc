import maya.api.OpenMaya as om2
import maya.OpenMaya as om




def get_mobject(node):
	selectionList = om2.MSelectionList()
	selectionList.add(node)
	oNode = om2.MObject()
	oNode = selectionList.getDependNode(0)
	return oNode

def get_skin_dag_path_and_mobject(skin):
	"""Returns the dagPath and MObject from the skin set."""
	function_set = om.MFnSet(skin.deformerSet())
	selection_list = om.MSelectionList()
	function_set.getMembers(selection_list, False)
	dag_p = om.MDagPath()
	mObj = om.MObject()
	selection_list.getDagPath(0, dag_p, mObj)
	return dag_p, mObj
