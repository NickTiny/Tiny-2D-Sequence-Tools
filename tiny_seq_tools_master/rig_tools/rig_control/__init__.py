from tiny_seq_tools_master.rig_tools.rig_control import ops, ui


def register():
    ops.register()
    ui.register()


def unregister():
    ops.unregister()
    ui.unregister()
