from unittest.mock import NonCallableMagicMock
from tiny_seq_tools_master.constraint_to_cams.core import constraints_to_active_camera
from tiny_seq_tools_master.line_art_tools.core import sync_update_line_art_objs
from tiny_seq_tools_master.scene_strip_tools.core import (
    sync_seq_camera_to_viewport,
    sync_selection_to_viewport,
)

import bpy
from operator import attrgetter

OldStrip = ""


def update_constraint_camera(scene):
    global OldStrip
    scn = scene
    if scn.sequence_editor is None:
        return
    seq = scn.sequence_editor.sequences
    seq = sorted(seq, key=attrgetter("channel", "frame_final_start"))
    cf = scn.frame_current
    for i in seq:
        try:
            if i.type == "SCENE" and i.name != OldStrip:
                if i.frame_final_start <= cf and i.frame_final_end > cf and not i.mute:
                    constraints_to_active_camera(i)
                    # sync_update_line_art_objs(i) disabled because of LINEARTCAMBUG
                    if (
                        i.scene.name == scene.name
                    ):  # Only if current scene in scene-strip

                        sync_seq_camera_to_viewport(i)
                        sync_selection_to_viewport(i)
                        oldStrip = i.name
                        break
        except AttributeError:
            pass


@bpy.app.handlers.persistent
def constraint_to_camera_handler(self, context):
    update_constraint_camera(self)


def register():
    bpy.app.handlers.frame_change_pre.append(constraint_to_camera_handler)


def unregister():
    bpy.app.handlers.frame_change_pre.remove(constraint_to_camera_handler)
