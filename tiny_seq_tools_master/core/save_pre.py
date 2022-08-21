import bpy
from bpy.app.handlers import persistent

from tiny_seq_tools_master.line_art_tools.line_art_cam.core import (
    refresh_line_art_on_save,
)


@persistent
def run_on_save(
    self,
):
    refresh_line_art_on_save()


def register():
    if not run_on_save in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_pre.append(run_on_save)


def unregister():
    if not run_on_save in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_pre.append(run_on_save)
