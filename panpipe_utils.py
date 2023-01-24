import bpy
from flute_parameters import BASE_FLUTE_NAME, FINGER_HOLE_NAME
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)


def get_base_flute():
    return bpy.data.objects[BASE_FLUTE_NAME]


def get_finger_hole():
    return bpy.data.objects[FINGER_HOLE_NAME]


# we load the base flute parameters at the beginning of the run to avoid object selection issues
BASE_FLUTE_HEIGHT = get_base_flute().dimensions.z
BASE_FLUTE_DEPTH = get_base_flute().dimensions.y


def select_base_flute_only() -> None:
    bpy.ops.object.select_all(action="DESELECT")
    get_base_flute().select_set(True)


def select_finger_hole_only() -> None:
    bpy.ops.object.select_all(action="DESELECT")
    get_finger_hole().select_set(True)


def duplicate_base_flute() -> bpy.types.Object:
    select_base_flute_only()
    bpy.ops.object.duplicate(linked=False)
    return bpy.context.selected_objects[0]


def save_stl(object_to_save: bpy.types.Object, filepath: str) -> None:
    bpy.ops.object.select_all(action="DESELECT")
    get_base_flute().select_set(False)  # do not save the base flute to the stl file
    get_finger_hole().select_set(False)  # do not save the base flute to the stl file
    bpy.context.view_layer.objects.active = object_to_save
    object_to_save.select_set(True)
    bpy.ops.export_mesh.stl(filepath=filepath, use_selection=True)


def select_vertex_group(blender_object: bpy.types.Object, vertex_group: bpy.types.VertexGroup) -> None:
    blender_object.vertex_groups.active = vertex_group
    bpy.ops.object.vertex_group_select()
