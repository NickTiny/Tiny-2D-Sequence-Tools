"""The Line Art Cam folder is made to cover a bug in line art, some of the code is not ideal but servicable until the bug is patched"""
#https://developer.blender.org/T100596

from tiny_seq_tools_master.line_art_tools import line_art_cam
from tiny_seq_tools_master.line_art_tools.line_art_cam.core import (
    update_line_art_override_cam_from_sequence,
    get_line_art_override_cam_from_strip,
)

import bpy


class SEQUENCER_OT_update_line_art_cam(bpy.types.Operator):
    bl_idname = "view3d.update_line_art_cam"
    bl_label = "Refresh Line Art Camera"
    bl_options  = {'UNDO'}

    def execute(self, context):
        strip = context.active_sequence_strip
        scene = strip.scene
        status = update_line_art_override_cam_from_sequence(scene)
        if not status:
            self.report({"ERROR"}, "Update Failed")
            return {"CANCELLED"}
        line_art_cam = get_line_art_override_cam_from_strip(strip)
        for obj in context.scene.objects:
            if obj.line_art_seq_obj:
                obj.grease_pencil_modifiers[0].source_camera = line_art_cam
        self.report(
            {"INFO"}, f"Line Art Override Camera:'{line_art_cam.name}' is up to date."
        )
        return {"FINISHED"}


classes = (SEQUENCER_OT_update_line_art_cam,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
