from tiny_seq_tools_master import (
    line_art_tools,
    tiny_status_tools,
    constraint_to_cams,
    scene_strip_tools,
    rig_tools,
    core,
)

bl_info = {
    "name": "Tiny Sequencer Tools",
    "author": "Nick Alberelli ",
    "description": "Tools for creating cut-out animation with Tiny's BLOWN APART Characters and Backgrounds",
    "blender": (3, 2, 0),
    "version": (1, 0, 7),
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
    rig_tools.register()


def unregister():
    line_art_tools.unregister()
    constraint_to_cams.unregister()
    tiny_status_tools.unregister()
    scene_strip_tools.unregister()
    core.unregister()
    rig_tools.unregister()
