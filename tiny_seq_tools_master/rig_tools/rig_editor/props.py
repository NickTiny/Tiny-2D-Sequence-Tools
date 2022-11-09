import bpy

classes = ()


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Object.offset_action = bpy.props.PointerProperty(
        name="Offset Action", type=bpy.types.Action
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Object.offset_action
