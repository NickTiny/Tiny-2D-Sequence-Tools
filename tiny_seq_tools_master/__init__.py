from tiny_seq_tools_master import (
    line_art_tools,
    tiny_status_tools,
    constraint_to_cams,
    scene_strip_tools,
    core,
)

bl_info = {
    "name": "Tiny 2D Sequence Tools",
    "author": "Nick Alberelli ",
    "description": "Tools for creating multi-cam 2d animation sequences with Line Art",
    "blender": (3, 3, 0),
    "version": (1, 1, 0,),
    "location": "Sequencer > Sidebar > Tiny Sequencer Tools",
    "warning": "",
    "category": "Sequencer",
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
