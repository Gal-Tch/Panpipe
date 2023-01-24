import bpy
import logging
from panpipe_utils import duplicate_base_flute, select_vertex_group, BASE_FLUTE_DEPTH
from flute_parameters import HEAD_DEPTH, INNER_CHAMBER_GAP, END_VERTEX_GROUP_NAME, BIAS

logger = logging.getLogger(__name__)


class FluteAdder:
    def __init__(self, flute_number: int, flute_length: float, xz_dimensions: float, panpipe: bpy.types.Object = None):
        self.flute_object = duplicate_base_flute()
        self.flute_number = flute_number
        self.flute_length = flute_length + BIAS
        self.flute_xz_dimensions = xz_dimensions
        self.panpipe = panpipe

    def rename_flute_vertex_groups(self) -> None:
        for vertex_group in self.flute_object.vertex_groups:
            vertex_group.name = f"{self.flute_object.name}_{vertex_group.name}"

    def merge_to_panpipe(self) -> bpy.types.Object:
        logger.info(f"Merging object {self.flute_object.name} with {self.panpipe.name}")

        # store objects original names
        new_flute_object_name = self.flute_object.name
        original_flute_object_name = self.panpipe.name

        # select the objects to merge
        # bpy.ops.mesh.select_all(action="DESELECT")
        self.flute_object.select_set(True)
        self.panpipe.select_set(True)

        bpy.context.view_layer.objects.active = self.flute_object

        bpy.ops.object.join()
        merged_panpipe = bpy.context.active_object

        bpy.ops.object.mode_set(mode="EDIT")
        for vertex_group in merged_panpipe.vertex_groups:
            bpy.ops.mesh.select_all(action="DESELECT")
            if vertex_group.name.startswith(f"{original_flute_object_name}_top_"):
                select_vertex_group(blender_object=merged_panpipe, vertex_group=vertex_group)
                parallel_vertex = merged_panpipe.vertex_groups[f"{new_flute_object_name}_bot_{vertex_group.name[-1]}"]
                select_vertex_group(blender_object=merged_panpipe, vertex_group=parallel_vertex)
                bpy.ops.mesh.merge(type="CENTER")
        bpy.ops.object.mode_set(mode="OBJECT")
        return merged_panpipe

    def set_flute_location(self) -> None:
        flute_z_location = self.flute_number * self.flute_xz_dimensions
        logger.info(f"Setting flute {self.flute_number} location to {0,0,flute_z_location} ")
        self.flute_object.location.x = 0
        self.flute_object.location.y = 0
        # to stack up the flutes at the right position
        self.flute_object.location.z = flute_z_location

    def set_flute_length(self) -> None:
        current_flute_chamber_length = BASE_FLUTE_DEPTH - HEAD_DEPTH - INNER_CHAMBER_GAP

        required_shift = self.flute_length - current_flute_chamber_length
        logger.info(f"Setting flute {self.flute_number} length to {self.flute_length + current_flute_chamber_length}")

        bpy.context.view_layer.objects.active = self.flute_object

        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="DESELECT")
        select_vertex_group(
            blender_object=self.flute_object, vertex_group=self.flute_object.vertex_groups[END_VERTEX_GROUP_NAME]
        )
        bpy.ops.transform.translate(
            value=(0, required_shift, 0), constraint_axis=(False, True, False), orient_type="GLOBAL"
        )
        bpy.ops.object.mode_set(mode="OBJECT")

    def set_flute_dimensions(self):
        logger.info(f"Setting flute {self.flute_number} xz dimensions to {self.flute_xz_dimensions}")
        self.flute_object.dimensions = (
            self.flute_xz_dimensions,
            self.flute_object.dimensions.y,
            self.flute_xz_dimensions,
        )

    def create_new_flute(self) -> bpy.types.Object:
        # rename the new flute object, initialize its location
        self.flute_object.name = f"flute_{self.flute_number}"
        self.set_flute_dimensions()
        self.set_flute_location()
        self.set_flute_length()
        # we rename the vertex groups to avoid naming collisions when merging flutes objects together
        self.rename_flute_vertex_groups()

    def add_flute_to_panpipe(self) -> bpy.types.Object:
        self.create_new_flute()
        if self.panpipe:
            return self.merge_to_panpipe()
        return self.flute_object
