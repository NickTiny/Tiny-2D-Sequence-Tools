from tiny_seq_tools_master import (
    line_art_tools,
    tiny_status_tools,
    constraint_to_cams,
)
from tiny_seq_tools_master.sync import sync_core, save_pre

bl_info = {
    "name": "constraint_to_strip_camera",
    "author": "Nick Alberelli ",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 2),
    "location": "",
    "warning": "",
    "category": "Generic",
}


from bpy.utils import register_class, unregister_class


def register():

    line_art_tools.register()
    constraint_to_cams.register()
    tiny_status_tools.register()
    sync_core.register()
    save_pre.register()


def unregister():
    sync_core.register()
    line_art_tools.unregister()
    constraint_to_cams.unregister()
    tiny_status_tools.unregister()
    sync_core.unregister()
    save_pre.unregister()
