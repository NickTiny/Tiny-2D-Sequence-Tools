import bpy


def constraints_to_active_camera(
    strip: bpy.types.Sequence,
) -> bool:
    """Set Constraint target to active trip's camera"""
    if not bpy.context.window_manager.enable_rot_seq_cam:
        return
    rot_to_seq_cam_status = False
    for item in bpy.context.window_manager.rot_to_seq_cam_items:
        obj = item.object
        for constraint in obj.constraints:
            if constraint.type == "COPY_ROTATION":
                constraint.target = strip.scene_camera
                rot_to_seq_cam_status |= True
    return rot_to_seq_cam_status


def check_rot_to_cam_status(obj):
    for constraint in obj.constraints:
        if constraint.type == "COPY_ROTATION" and constraint.name == "ROT_TO_SEQ_CAM":
            return True
    else:
        return False


def set_rot_to_seq_cam(obj):
    const = obj.constraints.new("COPY_ROTATION")
    const.name = "ROT_TO_SEQ_CAM"
    const.use_x = False
    const.use_y = False
    const.use_z = True
    return const


def refresh_rot_to_cam_list(context, strip):
    rot_to_seq_cam_items = context.window_manager.rot_to_seq_cam_items

    # Clear seq cam list
    rot_to_seq_cam_items.clear()

    # Check for active strip type
    if not strip or strip.type != "SCENE":
        return

    # Build seq cam list
    for obj in strip.scene.objects:
        if obj not in [x.object for x in rot_to_seq_cam_items]:
            status = check_rot_to_cam_status(obj)
            if status is True:
                add_rot_to_cam_item = rot_to_seq_cam_items.add()
                add_rot_to_cam_item.object = obj
    return True
