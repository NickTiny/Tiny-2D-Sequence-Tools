import bpy

from tiny_seq_tools_master.constraint_to_cams.core import constraints_to_active_camera
from tiny_seq_tools_master.line_art_tools.core import sync_strip_camera_to_seq_line_art

from operator import attrgetter

OldStrip = ""



def find_scene_strip(edit_scene):
    seq = [strip for strip in edit_scene.sequence_editor.sequences if strip.type == "SCENE"]
    seq = sorted(seq, key=attrgetter("channel", "frame_final_start"))
    for strip in seq:
        current_keyframe = edit_scene.frame_current
        #current_keyframe = int(edit_scene.frame_current - strip.frame_start + strip.scene.frame_start)
        if strip.frame_final_start <= current_keyframe and strip.frame_final_end > current_keyframe:
            #OldStrip = strip.name
            return strip

def update_constraint_camera(scene):
    global OldStrip 
    try:
        from spa_sequencer.sync.core import (get_sync_settings)
        master_scene = get_sync_settings().master_scene
        strip = master_scene.sequence_editor.sequences[get_sync_settings().last_master_strip]
        if strip.name == OldStrip:
            return
        constraints_to_active_camera(strip)
        sync_strip_camera_to_seq_line_art(strip)
        OldStrip == strip.name
    except ModuleNotFoundError:
        return


@bpy.app.handlers.persistent
def constraint_to_camera_handler(self, context):
    update_constraint_camera(self)


def register():
    bpy.app.handlers.frame_change_pre.append(constraint_to_camera_handler)


def unregister():
    bpy.app.handlers.frame_change_pre.remove(constraint_to_camera_handler)
