from . import (
    line_art_tools,
    constraint_to_camera,
)

bl_info = {
    "name": "constraint_to_strip_camera",
    "author": "Nick Alberelli ",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic",
}


from bpy.utils import register_class, unregister_class


def register():
    line_art_tools.register()
    constraint_to_camera.register()


def unregister():
    line_art_tools.unregister()
    constraint_to_camera.unregister()
