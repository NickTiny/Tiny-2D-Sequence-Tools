import bpy


def register():
    bpy.types.Scene.link_seq_to_3d_view = bpy.props.BoolProperty(
        name="Link Sequencer to 3D View",
        description="Sync 3DViewport and Sequencer Strips",
        default=True,
    )
    bpy.types.Scene.selection_to_active = bpy.props.BoolProperty(
        name="Sync Playhead to Active",
        default=True,
        description="Sync Selection/Active to Playhead",
    )


def unregister():
    del bpy.types.Scene.link_seq_to_3d_view
    del bpy.types.Scene.selection_to_active
