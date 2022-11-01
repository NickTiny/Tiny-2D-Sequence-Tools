"""The Line Art Cam folder is made to cover a bug in line art, some of the code is not ideal but servicable until the bug is patched"""

import bpy


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
    line_art_cam.location = strip_camera.location
    line_art_cam.rotation_euler = strip_camera.rotation_euler
    line_art_cam.data.lens = strip_camera.data.lens
    line_art_cam.data.shift_x = strip_camera.data.shift_x
    line_art_cam.data.shift_y = strip_camera.data.shift_y
    line_art_cam.data.clip_start = strip_camera.data.clip_start
    line_art_cam.data.clip_end = strip_camera.data.clip_end
    keyframe_all_camera_data_paths(line_art_cam, frame)
    return


def update_line_art_override_cam_from_sequence(scene: bpy.types.Scene) -> bool:
    """Clear Line Art Override Camera and copy all strip cameras to Line Art Override Cam"""
    line_art_cam = get_line_art_override_cam_from_scene(scene)
    line_art_cam.animation_data_clear()
    line_art_cam.data.animation_data_clear()
    for strip in scene.sequence_editor.sequences_all:
        if strip.type == "SCENE":
            if strip.mute != True:

                if not line_art_cam:
                    return False
                for frame in range(strip.frame_final_start, strip.frame_final_end):
                    strip_camera = strip.scene_camera

                    if (line_art_cam.location != strip_camera.location) or (
                        line_art_cam.data.shift_x != strip_camera.data.shift_x
                    ):
                        copy_all_camera_data_paths(
                            scene, frame, strip_camera, line_art_cam
                        )
                    else:
                        keyframe_all_camera_data_paths(
                            line_art_cam, strip.frame_final_start
                        )
                        keyframe_all_camera_data_paths(
                            line_art_cam, strip.frame_final_end - 1
                        )

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
        if scene.update_line_art_on_save and bpy.context.window_manager.line_art_cam_override:
            cur_frame = scene.frame_current
            print(f"CUR FRAME{cur_frame}")
            update_line_art_override_cam_from_sequence(scene)
            line_art_updated = True
            scene.frame_set(frame=cur_frame)
            return line_art_updated
        try_set_current_keyframe(frame)
