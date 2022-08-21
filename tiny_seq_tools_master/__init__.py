from tiny_seq_tools_master import (
    line_art_tools,
    tiny_status_tools,
    constraint_to_cams,
    scene_strip_tools,
    core,
)

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


def register():
    line_art_tools.register()
    constraint_to_cams.register()
    tiny_status_tools.register()
    scene_strip_tools.register()
    core.register()


def unregister():
    line_art_tools.unregister()
    constraint_to_cams.unregister()
    tiny_status_tools.unregister()
    scene_strip_tools.unregister()
    core.unregister()
