import bpy
from bpy.app.handlers import persistent

from tiny_seq_tools_master.line_art_tools.line_art_cam.core import (
    refresh_line_art_on_save,
)

from tiny_seq_tools_master.tiny_status_tools.ops import  (draw_status_checker)

@persistent
def run_on_save(
    self,
):
    refresh_line_art_on_save()

@persistent
def run_tiny_status(self):
    tiny_status = bpy.context.scene.tiny_status
    for prop in [tiny_status.file_path_status, tiny_status.relative_links, tiny_status.render_passes, tiny_status.pack_status]:
        if prop == False:
            bpy.context.window_manager.popup_menu(
                    draw_status_checker, title="One or more requirements is missing to save for collaboration.", icon='ERROR'
                )

def register():
    if not run_on_save in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_pre.append(run_on_save)
    bpy.app.handlers.save_pre.append(run_tiny_status)
    
        


def unregister():
    if not run_on_save in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_pre.append(run_on_save)
    bpy.app.handlers.save_pre.remove(run_tiny_status)
