import bpy
from bpy.app.handlers import persistent

from tiny_seq_tools_master.constraint_to_cams.core import (
    refresh_rot_to_cam_list,
)


@persistent
def load_handler(
    self,
):
    context = bpy.context
    for strip in [
        strip
        for strip in context.scene.sequence_editor.sequences_all
        if strip.type == "SCENE"
    ]:
        refresh_rot_to_cam_list(context, strip)


def register():
    bpy.app.handlers.load_post.append(load_handler)


def unregister():
    bpy.app.handlers.load_post.append(load_handler)
