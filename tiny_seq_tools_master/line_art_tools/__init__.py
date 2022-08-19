from line_art_tools import ops, props, ui


def register():
    ops.register()
    props.register()
    ui.register()


def unregister():
    ops.unregister()
    props.unregister()
    ui.unregister()
