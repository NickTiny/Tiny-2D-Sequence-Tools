"""The Line Art Cam folder is made to cover a bug in line art, some of the code is not ideal but servicable until the bug is patched"""

import bpy

from tiny_seq_tools_master.constraint_to_cams.core import refresh_rot_to_cam_list


def get_line_art_override_cam_from_scene(scene: bpy.types.Scene) -> bpy.types.Object:
    """Find Line Art Override Camera within a scene"""
    line_art_cam_name = scene.line_art_cam_name
    for obj in scene.objects:
        if obj.name == line_art_cam_name:
            line_art_cam = obj
            print("LINE ART CAM FOUND")
            return line_art_cam

    # create a new line art cam if none is found
    else:
        line_art_cam_data = bpy.data.cameras.new(line_art_cam_name)
        line_art_cam = bpy.data.objects.new(f"{line_art_cam_name}", line_art_cam_data)
        scene.collection.objects.link(line_art_cam)
        print("LINE ART CAM CREATED")
        return line_art_cam


def get_line_art_override_cam_from_strip(strip: bpy.types.Sequence) -> bpy.types.Object:
    """Find Line Art Override Camera from a strip's scene"""
    # cancel if strip is not a scene strip
    if strip.type != "SCENE":
        return

    # Get line art override cam from strip's scene
    line_art_cam = get_line_art_override_cam_from_scene(strip.scene)
    return line_art_cam


def keyframe_all_camera_data_paths(line_art_cam: bpy.types.Object, frame: int):
    """Insert Keyframes on all data paths needed to animate to camera objects"""
    line_art_cam.keyframe_insert(data_path="location", frame=frame)
    line_art_cam.keyframe_insert(data_path="rotation_euler", frame=frame)
    line_art_cam.data.keyframe_insert(data_path="lens", frame=frame)
    line_art_cam.data.keyframe_insert(data_path="shift_x", frame=frame)
    line_art_cam.data.keyframe_insert(data_path="shift_y", frame=frame)
    line_art_cam.data.keyframe_insert(data_path="clip_start", frame=frame)
    line_art_cam.data.keyframe_insert(data_path="clip_end", frame=frame)
    return


def copy_all_camera_data_paths(
    scene: bpy.types.Scene,
    frame: int,
    strip_camera: bpy.types.Object,
    line_art_cam: bpy.types.Object,
):
    """Copy data from Source Camera to Line Art Camera on all data paths needed to animate camera objects"""
    scene.frame_set(frame)
    line_art_cam.matrix_local = strip_camera.matrix_world
    line_art_cam.data.lens = strip_camera.data.lens
    line_art_cam.data.shift_x = strip_camera.data.shift_x
    line_art_cam.data.shift_y = strip_camera.data.shift_y
    line_art_cam.data.clip_start = strip_camera.data.clip_start
    line_art_cam.data.clip_end = strip_camera.data.clip_end
    keyframe_all_camera_data_paths(line_art_cam, frame)
    return


def check_all_camera_data_paths_match(
    scene: bpy.types.Scene,
    frame: int,
    strip_camera: bpy.types.Object,
    line_art_cam: bpy.types.Object,
):
    """Copy data from Source Camera to Line Art Camera on all data paths needed to animate camera objects"""
    scene.frame_set(frame)
    if (
        line_art_cam.matrix_local == strip_camera.matrix_world
        and line_art_cam.data.lens == strip_camera.data.lens
        and line_art_cam.data.shift_x == strip_camera.data.shift_x
        and line_art_cam.data.shift_y == strip_camera.data.shift_y
        and line_art_cam.data.clip_start == strip_camera.data.clip_start
        and line_art_cam.data.clip_end == strip_camera.data.clip_end
    ):
        return True
    else:
        False


def save_camera_on_frame(scene, frame, strip_camera, line_art_cam):
    copy_all_camera_data_paths(scene, frame, strip_camera, line_art_cam)
    keyframe_all_camera_data_paths(line_art_cam, frame)


def update_line_art_override_cam_from_sequence(
    scene: bpy.types.Scene, override_rot: bool, update_viewport: bool
) -> bool:
    """Clear Line Art Override Camera and copy all strip cameras to Line Art Override Cam"""
    line_art_cam = get_line_art_override_cam_from_scene(scene)
    line_art_cam.animation_data_clear()
    line_art_cam.data.animation_data_clear()
    for strip in scene.sequence_editor.sequences_all:
        if strip.type == "SCENE":
            if strip.mute != True:
                if not line_art_cam:
                    return False
                strip_camera = strip.scene.camera
                save_camera_on_frame(
                    scene, strip.frame_final_start, strip_camera, line_art_cam
                )
                for frame in range(strip.frame_final_start, strip.frame_final_end - 1):
                    strip_camera = strip.scene_camera
                    if not check_all_camera_data_paths_match(
                        scene, frame, strip_camera, line_art_cam
                    ):
                        save_camera_on_frame(scene, frame, strip_camera, line_art_cam)
                save_camera_on_frame(
                    scene, strip.frame_final_end - 1, strip_camera, line_art_cam
                )
                if update_viewport:
                    bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)

    win_man = bpy.context.window_manager

    # Set 'Rot to Seq Cam' Items
    if override_rot:
        refresh_rot_to_cam_list(bpy.context, strip)
        win_man.enable_rot_seq_cam = False
        for item in win_man.rot_to_seq_cam_items:
            item.object.constraints["ROT_TO_STRIP_CAM"].target = line_art_cam

    # Set line art items
    win_man.line_art_cam_override = True
    for item in win_man.line_art_seq_items:
        item.object.grease_pencil_modifiers["SEQ_LINE_ART"].use_custom_camera = True
        item.object.grease_pencil_modifiers["SEQ_LINE_ART"].source_camera = line_art_cam

    return True


def try_get_current_keyframe() -> int:
    """Attempt to get current frame"""
    try:
        cur_frame = bpy.context.scene.frame_current
        return cur_frame
    except AttributeError:
        pass


def try_set_current_keyframe(frame: int) -> bool:
    """Attempt to set current frame"""
    try:
        bpy.context.scene.frame_set(frame)
        return True
    except AttributeError:
        pass


def refresh_line_art_on_save() -> bool:
    """Function to be called by pre save handler.
    Refresh line art override camera at save"""
    scenes = bpy.data.scenes
    frame = try_get_current_keyframe()
    line_art_updated = False
    avl_scenes = [scene for scene in scenes if scene.name != "RENDER"]
    for scene in avl_scenes:
        if (
            scene.update_line_art_on_save
            and bpy.context.window_manager.line_art_cam_override
        ):
            cur_frame = scene.frame_current
            print(f"CUR FRAME{cur_frame}")
            update_line_art_override_cam_from_sequence(scene)
            line_art_updated = True
            scene.frame_set(frame=cur_frame)
            return line_art_updated
        try_set_current_keyframe(frame)
