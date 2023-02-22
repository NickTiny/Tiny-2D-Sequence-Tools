import bpy

from tiny_seq_tools_master.constraint_to_cams.core import constraints_to_active_camera
from tiny_seq_tools_master.line_art_tools.core import sync_strip_camera_to_seq_line_art


OldStrip = ""

def update_constraint_camera(scene):
    global OldStrip 
    try:
        from spa_sequencer.sync.core import (get_sync_settings)
        if not get_sync_settings().master_scene:
            return
        master_scene = get_sync_settings().master_scene
        strip = master_scene.sequence_editor.sequences.get(get_sync_settings().last_master_strip)
        if strip is None or strip.name == OldStrip:
            return
        constraints_to_active_camera(strip)
        sync_strip_camera_to_seq_line_art(strip)
        OldStrip = strip.name
    except ModuleNotFoundError:
        return


@bpy.app.handlers.persistent
def constraint_to_camera_handler(self, context):
    update_constraint_camera(self)


def register():
    bpy.app.handlers.frame_change_pre.append(constraint_to_camera_handler)


def unregister():
    bpy.app.handlers.frame_change_pre.remove(constraint_to_camera_handler)
