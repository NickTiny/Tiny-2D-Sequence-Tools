"""The Line Art Cam folder is made to cover a bug in line art, some of the code is not ideal but servicable until the bug is patched"""

import bpy


def register():
    bpy.types.Scene.line_art_cam_name = bpy.props.StringProperty(
        name="Line Art Cam Name", default="TINY LINE ART CAM"
    )
    bpy.types.Scene.update_line_art_on_save = bpy.props.BoolProperty(
        name="Update Line Art on Save", default=True
    )


def unregister():
    del bpy.types.Scene.line_art_cam_name
    del bpy.types.Scene.update_line_art_on_save
