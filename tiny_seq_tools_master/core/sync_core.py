import bpy

from tiny_seq_tools_master.constraint_to_cams.core import constraints_to_active_camera
from tiny_seq_tools_master.line_art_tools.core import sync_strip_camera_to_seq_line_art

def update_constraint_camera(scene):
    try:
        from spa_sequencer.sync.core import (get_sync_master_strip)
        strip, _= get_sync_master_strip()
        constraints_to_active_camera(strip)
        sync_strip_camera_to_seq_line_art(strip)   
    except ModuleNotFoundError:
        return


@bpy.app.handlers.persistent
def constraint_to_camera_handler(self, context):
    update_constraint_camera(self)


def register():
    bpy.app.handlers.frame_change_pre.append(constraint_to_camera_handler)


def unregister():
    bpy.app.handlers.frame_change_pre.remove(constraint_to_camera_handler)
