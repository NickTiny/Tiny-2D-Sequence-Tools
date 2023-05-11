from tiny_seq_tools_master.rig_tools.rig_editor import ops, ui, props, prefs


def register():
    ops.register()
    ui.register()
    props.register()
    prefs.register()


def unregister():
    ops.unregister()
    ui.unregister()
    props.unregister()
    prefs.unregister()
