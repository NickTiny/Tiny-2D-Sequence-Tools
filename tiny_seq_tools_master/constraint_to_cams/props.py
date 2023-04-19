import bpy


class rot_to_seq_cam_items(bpy.types.PropertyGroup):
    object: bpy.props.PointerProperty(type=bpy.types.Object)


classes = (rot_to_seq_cam_items,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.rot_to_seq_cam_items = bpy.props.CollectionProperty(
        type=rot_to_seq_cam_items
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.WindowManager.rot_to_seq_cam_items
