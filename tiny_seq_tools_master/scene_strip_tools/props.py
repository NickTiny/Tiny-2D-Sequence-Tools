import bpy


def register():
    bpy.types.Scene.link_seq_to_3d_view = bpy.props.BoolProperty(
        name="Enable Rotate to Strip Cameras",
        default=True,
    )
    bpy.types.Scene.selection_to_active = bpy.props.BoolProperty(
        name="Sync Playhead to Active",
        default=True,
    )


def unregister():
    del bpy.types.Scene.link_seq_to_3d_view
    del bpy.types.Scene.selection_to_active
