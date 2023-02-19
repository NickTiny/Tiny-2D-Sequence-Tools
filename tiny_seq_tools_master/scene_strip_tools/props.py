import bpy


class TINYSEQ_SCENE_STRIP_TOOLS(bpy.types.PropertyGroup):
    render_preview_range: bpy.props.BoolProperty(
        name="Render Preview Range",
        default=False,
        description="Hide and Show Line Art Modifiers in Viewports",
        )

    render_start: bpy.props.IntProperty (name="Start", default=1)
    render_end: bpy.props.IntProperty (name="End", default=250)




classes = (TINYSEQ_SCENE_STRIP_TOOLS,)

def register():
    for cls in (classes):
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.render_settings = bpy.props.PointerProperty(type=TINYSEQ_SCENE_STRIP_TOOLS)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.WindowManager.render_settings
    
