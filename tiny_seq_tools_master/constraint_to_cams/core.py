import bpy


def constraints_to_active_camera(
    strip: bpy.types.Sequence,
):
    for item in strip.id_data.rot_to_seq_cam_items:
        obj = item.object
        for constraint in obj.constraints:
            if constraint.type == "COPY_ROTATION":
                constraint.target = strip.scene_camera
