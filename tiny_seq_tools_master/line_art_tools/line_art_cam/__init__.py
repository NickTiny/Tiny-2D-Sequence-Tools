from tiny_seq_tools_master.line_art_tools.line_art_cam import ops, props

## This exists to cover a bug in line art that it wont' render from a custom camera
## Look for LINEARTCAMBUG to find related uses outside LINE_ART_CAM folder


def register():
    ops.register()
    props.register()


def unregister():
    ops.unregister()
    props.unregister()
