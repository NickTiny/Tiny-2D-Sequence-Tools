import bpy


def register():
    bpy.types.Scene.link_seq_to_3d_view = bpy.props.BoolProperty(
        name="Enable Rotate to Strip Cameras",
        default=False,
    )


def unregister():
    del bpy.types.Scene.link_seq_to_3d_view
