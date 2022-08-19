# def update_line_art_objs(strip):
#     for obj in strip.scene.objects:
#         if obj.line_art_seq_cam is True:
#             for mod in obj.grease_pencil_modifiers:
#                 if mod.type == "GP_LINEART":
#                     mod.source_camera = strip.scene_camera
import bpy


def constraints_to_active_camera(
    strip: bpy.types.Sequence,
):
    for item in strip.id_data.rot_to_seq_cam_items:
        obj = item.object
        for constraint in obj.constraints:
            if constraint.type == "COPY_ROTATION":
                constraint.target = strip.scene_camera
