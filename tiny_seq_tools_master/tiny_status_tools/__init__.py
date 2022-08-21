from tiny_seq_tools_master.tiny_status_tools import ops, ui, props


def register():
    ops.register()
    ui.register()
    props.register()


def unregister():
    ops.unregister()
    ui.unregister()
    props.unregister()
