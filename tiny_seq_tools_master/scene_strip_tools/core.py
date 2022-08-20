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

# oldStrip = ""


# def set3d_view_global():
#     for area in bpy.context.screen.areas:
#         if area.type == "VIEW_3D":
#             space = area.spaces[0]
#             if space.local_view:  # check if using local view
#                 for region in area.regions:
#                     if region.type == "WINDOW":
#                         override = {"area": area, "region": region}  # override context
#                         bpy.ops.view3d.localview(override)  # switch to global view


def sync_seq_camera_to_viewport(i):
    updated_viewport = False
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            bpy.context.scene.camera = bpy.data.objects[
                i.scene_camera.name
            ]  # Select camera as view
            area.spaces.active.region_3d.view_perspective = "CAMERA"  # Use camera view
            updated_viewport = True
    return updated_viewport


# def swich_camera_at_frame_change():

#     if bpy.context.scene.asset_manager.link_seq_to_3d_view != True:
#         return

#     global oldStrip
#     scn = bpy.context.scene
#     seq = scn.sequence_editor.sequences
#     seq = sorted(seq, key=attrgetter("channel", "frame_final_start"))
#     cf = scn.frame_current

#     for i in seq:
#         try:
#             if i.type == "SCENE" and i.name != oldStrip:
#                 if (
#                     i.frame_final_start <= cf
#                     and i.frame_final_end > cf
#                     and i.scene.name
#                     == bpy.context.scene.name  # Only if current scene in scene-strip
#                     and not i.mute
#                 ):
#                     if sync_seq_camera_to_viewport(i):
#                         oldStrip = i.name
#                     break

#         except AttributeError:
#             pass


# @bpy.app.handlers.persistent
# def attach_as_handler(self, context):
#     swich_camera_at_frame_change()


def make_render_scene(context):
    scene_name = "RENDER"
    user_scene_name = str(context.scene.name)
    for scene in bpy.data.scenes:
        if scene.name == scene_name:
            bpy.ops.scene.delete({"scene": bpy.data.scenes[scene_name]})

    bpy.ops.scene.new("INVOKE_DEFAULT", type="EMPTY")
    bpy.context.scene.sequence_editor_create()
    bpy.context.scene.name = scene_name
    render_scene = bpy.data.scenes[scene_name]
    context.window.scene = bpy.data.scenes[f"{user_scene_name}"]

    # Copy Strips
    context.scene.frame_set(1)
    bpy.ops.sequencer.select_all(action="SELECT")
    bpy.ops.sequencer.copy()

    # Paste Strips
    context.window.scene = render_scene
    context.scene.frame_set(1)
    bpy.ops.sequencer.paste()
    context.window.scene = bpy.data.scenes[f"{user_scene_name}"]
    return render_scene, user_scene_name


def menu_toggle_scene(self, context):
    self.layout.separator()
    self.layout.operator("sequencer.change_scene")


def menu_add_camera(self, context):
    self.layout.operator("view3d.add_scene_strip", icon="VIEW_CAMERA")


def menu_link_tdview(self, context):
    layout = self.layout
    col = layout.column(align=(False))
    # col = col.use_property_split = True
    # col = col.alignment = 'RIGHT'
    manager = context.scene.asset_manager
    col.prop(manager, "link_seq_to_3d_view", text="Link Sequencer to 3D Viewport")


def menu_convert_markers(self, context):
    self.layout.separator()
    self.layout.operator("sequencer.convert_cameras")


def register():
    # bpy.app.handlers.frame_change_pre.append(attach_as_handler)
    bpy.types.SEQUENCER_MT_strip.append(menu_toggle_scene)
    bpy.types.SEQUENCER_MT_context_menu.append(menu_toggle_scene)
    bpy.types.SEQUENCER_HT_header.append(menu_link_tdview)
    bpy.types.SEQUENCER_MT_add.prepend(menu_add_camera)
    bpy.types.SEQUENCER_MT_marker.append(menu_convert_markers)


def unregister():
    bpy.types.SEQUENCER_MT_strip.remove(menu_toggle_scene)
    bpy.types.SEQUENCER_MT_context_menu.remove(menu_toggle_scene)
    bpy.types.SEQUENCER_HT_header.remove(menu_link_tdview)
    bpy.types.SEQUENCER_MT_add.remove(menu_add_camera)
    bpy.types.SEQUENCER_MT_marker.remove(menu_convert_markers)
    # bpy.app.handlers.frame_change_pre.remove(attach_as_handler)
