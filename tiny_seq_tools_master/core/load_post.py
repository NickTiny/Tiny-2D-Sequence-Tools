import bpy
from bpy.app.handlers import persistent

from tiny_seq_tools_master.constraint_to_cams.core import (
    refresh_rot_to_cam_list,
)


@persistent
def load_handler(
    self,
):  
    try:
        from spa_sequencer.sync.core import (get_sync_settings)
        if not get_sync_settings().master_scene:
            return
        master_scene = get_sync_settings().master_scene
        context = bpy.context
        scene = context.window_manager.timeline_sync_settings.master_scene
        strips = [
            strip
            for strip in scene.sequence_editor.sequences_all
            if strip.type == "SCENE"
        ]
        refresh_rot_to_cam_list(context, strips)
    except ModuleNotFoundError:
        return


def register():
    bpy.app.handlers.load_post.append(load_handler)


def unregister():
    bpy.app.handlers.load_post.append(load_handler)
