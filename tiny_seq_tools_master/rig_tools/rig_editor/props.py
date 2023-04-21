import bpy

classes = ()


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.target_armature = bpy.types.PointerProperty(bpy.types.Armature)
    bpy.types.WindowManager.offset_editor_active = bpy.props.BoolProperty(
        name="Offset Editor is Active", default=False
    )
    bpy.types.WindowManager.gpencil_editor_active = bpy.props.PointerProperty(
        type=bpy.types.GreasePencil
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    #TODO del properties 
