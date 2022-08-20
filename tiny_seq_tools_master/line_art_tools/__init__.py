from tiny_seq_tools_master.line_art_tools import ops, props, ui, line_art_cam


def register():
    ops.register()
    props.register()
    ui.register()
    line_art_cam.register()  ## Exists because of LINEARTCAMBUG


def unregister():
    ops.unregister()
    props.unregister()
    ui.unregister()
    line_art_cam.unregister()  ## Exists because of LINEARTCAMBUG
