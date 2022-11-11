import bpy

classes = ()


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.offset_editor_active = bpy.props.BoolProperty(
        name="Offset Editor is Active", default=False
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
