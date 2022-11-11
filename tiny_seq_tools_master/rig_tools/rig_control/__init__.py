from tiny_seq_tools_master.rig_tools.rig_control import ops, ui, props


def register():
    ops.register()
    ui.register()
    props.register()


def unregister():
    ops.unregister()
    ui.unregister()
    props.unregister()
