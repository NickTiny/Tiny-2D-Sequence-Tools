from tiny_seq_tools_master.line_art_tools import line_art_cam
from tiny_seq_tools_master.line_art_tools.line_art_cam.core import (
    update_line_art_camera_from_sequence,
    get_line_art_cam_from_strip,
)

import bpy


class SEQUENCER_OT_update_line_art_cam(bpy.types.Operator):
    bl_idname = "view3d.update_line_art_cam"
    bl_label = "Refresh Line Art Camera"

    def execute(self, context):
        strip = context.active_sequence_strip
        scene = strip.scene
        status = update_line_art_camera_from_sequence(scene)
        if not status:
            self.report({"ERROR"}, "Update Failed")
            return {"CANCELLED"}
        line_art_cam = get_line_art_cam_from_strip(strip)
        for obj in context.scene.objects:
            if obj.line_art_seq_cam:
                obj.grease_pencil_modifiers["Line Art"].source_camera = line_art_cam

        return {"FINISHED"}


classes = (SEQUENCER_OT_update_line_art_cam,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
