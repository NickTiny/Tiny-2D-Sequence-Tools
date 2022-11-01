import bpy


def constraints_to_active_camera(
    strip: bpy.types.Sequence,
) -> bool:
    """Set Constraint target to active trip's camera"""

    rot_to_seq_cam_status = False
    for item in bpy.context.window_manager.rot_to_seq_cam_items:
        obj = item.object
        for constraint in obj.constraints:
            if constraint.type == "COPY_ROTATION":
                constraint.target = strip.scene_camera
                rot_to_seq_cam_status |= True
    return rot_to_seq_cam_status
