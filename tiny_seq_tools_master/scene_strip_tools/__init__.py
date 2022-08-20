from tiny_seq_tools_master.scene_strip_tools import core, ops, ui


def register():
    ops.register()
    ui.register()


def unregister():
    ops.unregister()
    ui.unregister()
