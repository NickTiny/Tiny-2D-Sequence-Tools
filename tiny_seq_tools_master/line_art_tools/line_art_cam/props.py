import bpy


def register():
    bpy.types.Scene.line_art_cam_name = bpy.props.StringProperty(
        name="Line Art Cam Name", default="TINY LINE ART CAM"
    )


def unregister():
    del bpy.types.Scene.line_art_cam_name
