import bpy

from lib2to3.pgen2.token import STAREQUAL
import bpy
import mathutils
from mathutils import Matrix
from bpy.utils import register_class, unregister_class
from bpy.props import BoolProperty, EnumProperty
from bpy.types import Panel, Menu
from rna_prop_ui import PropertyPanel
from operator import attrgetter


class SEQUENCER_PT_scene_tools(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_scene_tools"
    bl_label = "Scene Strip Tools"
    bl_category = "Scene Strip Tools"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=(False))
        col = col.box()
        manager = context.scene

        col.prop(
            manager,
            "link_seq_to_3d_view",
            text="Link Sequencer to 3D Viewport",
            icon="LINKED",
        )
        col.operator(
            "view3d.add_scene_strip",
            text="Add Camera as Scene Strip",
            icon="CAMERA_DATA",
        )
        col.operator(
            "sequencer.convert_cameras",
            text="Convert Camera Markers to Strips",
            icon="MARKER",
        )
        col.operator("sequencer.change_scene", text="Toggle Scene Strip", icon="VIEW3D")

        col = layout.box()
        col.label(text="Render Strips")

        col.prop(
            context.scene.render,
            "filepath",
            text="Output",
        )

        col.operator("sequencer.preview_render", icon="FILE_MOVIE")
        set_row = col.row(align=True)
        set_row.operator("sequencer.batch_render", icon="RENDER_ANIMATION")
        set_row.operator("sequencer.setup_render", icon="SCENE_DATA", text="")


classes = (SEQUENCER_PT_scene_tools,)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
