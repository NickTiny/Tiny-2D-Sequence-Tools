from tiny_seq_tools_master.tiny_status_tools import ops, props


def register():
    ops.register()
    props.register()


def unregister():
    ops.unregister()
    props.unregister()
