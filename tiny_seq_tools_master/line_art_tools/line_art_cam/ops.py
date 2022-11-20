"""The Line Art Cam folder is made to cover a bug in line art, some of the code is not ideal but servicable until the bug is patched"""
# https://developer.blender.org/T100596

from tiny_seq_tools_master.line_art_tools import line_art_cam
from tiny_seq_tools_master.line_art_tools.line_art_cam.core import (
    update_line_art_override_cam_from_sequence,
)

import bpy


class SEQUENCER_OT_update_line_art_cam(bpy.types.Operator):
    bl_idname = "view3d.update_line_art_cam"
    bl_label = "Bake Seq Camera"
    bl_options = {"REGISTER", "UNDO"}

    override_rot_to_seq: bpy.props.BoolProperty(
        name="Include Rotate to Camera in Override/Bake", default=False
    )
    update_viewport: bpy.props.BoolProperty(
        name="Update Viewport while Running Operation", default=True
    )

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        self.layout.prop(self, "override_rot_to_seq")
        self.layout.prop(self, "update_viewport")

    def execute(self, context):
        strip = context.active_sequence_strip
        scene = strip.scene
        status = update_line_art_override_cam_from_sequence(
            scene, self.override_rot_to_seq, self.update_viewport
        )
        if not status:
            self.report({"ERROR"}, "Update Failed")
            return {"CANCELLED"}
        self.report({"INFO"}, f"Camera is baked.")
        return {"FINISHED"}


classes = (SEQUENCER_OT_update_line_art_cam,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
