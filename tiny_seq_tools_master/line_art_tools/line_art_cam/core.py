import bpy

line_art_cam_name = "TINY LINE ART CAM"


def get_line_art_from_scene(scene):
    for obj in scene.objects:
        if obj.name == line_art_cam_name:
            line_art_cam = obj
            print("LINE ART CAM FOUND")
            return line_art_cam

    # create a new line art cam
    else:
        line_art_cam_data = bpy.data.cameras.new(line_art_cam_name)
        line_art_cam = bpy.data.objects.new(f"{line_art_cam_name}", line_art_cam_data)
        scene.collection.objects.link(line_art_cam)
        print("LINE ART CAM CREATED")
        return line_art_cam


def get_line_art_cam_from_strip(strip):
    # cancel if strip is not a scene strip
    if strip.type != "SCENE":
        return

    # get objects from a strip's scene, filter for line art cam
    # line_art_cam_name = strip.scene.line_art_cam_name
    line_art_cam = get_line_art_from_scene(strip.scene)
    return line_art_cam


def camera_keyframes(line_art_cam, frame):
    line_art_cam.keyframe_insert(data_path="location", frame=frame)
    line_art_cam.keyframe_insert(data_path="rotation_euler", frame=frame)
    line_art_cam.data.keyframe_insert(data_path="lens", frame=frame)
    line_art_cam.data.keyframe_insert(data_path="shift_x", frame=frame)
    line_art_cam.data.keyframe_insert(data_path="shift_y", frame=frame)
    line_art_cam.data.keyframe_insert(data_path="clip_start", frame=frame)
    line_art_cam.data.keyframe_insert(data_path="clip_end", frame=frame)
    return


def copy_camera_locations(line_art_cam, scene, cur, frame):
    scene.frame_set(frame)
    line_art_cam.location = cur.location
    line_art_cam.rotation_euler = cur.rotation_euler
    line_art_cam.data.lens = cur.data.lens
    line_art_cam.data.shift_x = cur.data.shift_x
    line_art_cam.data.shift_y = cur.data.shift_y
    line_art_cam.data.clip_start = cur.data.clip_start
    line_art_cam.data.clip_end = cur.data.clip_end
    camera_keyframes(line_art_cam, frame)
    return


def update_line_art_camera_from_sequence(scene):
    line_art_cam = get_line_art_from_scene(scene)
    line_art_cam.animation_data_clear()
    line_art_cam.data.animation_data_clear()
    for strip in scene.sequence_editor.sequences_all:
        if strip.type == "SCENE":
            if strip.mute != True:

                if not line_art_cam:
                    return False
                for frame in range(strip.frame_final_start, strip.frame_final_end):
                    cur = strip.scene_camera

                    if (line_art_cam.location != cur.location) or (
                        line_art_cam.data.shift_x != cur.data.shift_x
                    ):
                        copy_camera_locations(line_art_cam, scene, cur, frame)
                    else:
                        camera_keyframes(line_art_cam, strip.frame_final_start)
                        camera_keyframes(line_art_cam, strip.frame_final_end - 1)

    return True


def try_get_current_keyframe():
    try:
        cur_frame = bpy.context.scene.frame_current
        return cur_frame
    except AttributeError:
        pass


def try_set_current_keyframe(frame):
    try:
        bpy.context.scene.frame_set(frame)
        return True
    except AttributeError:
        pass


def refresh_line_art_on_save():
    frame = try_get_current_keyframe()
    scenes = bpy.data.scenes
    line_art_updated = False
    avl_scenes = [scene for scene in scenes if scene.name != "RENDER"]
    for scene in avl_scenes:
        cur_frame = scene.frame_current
        print(f"CUR FRAME{cur_frame}")
        update_line_art_camera_from_sequence(scene)
        line_art_updated = True
        scene.frame_set(frame=cur_frame)
        return line_art_updated
    try_set_current_keyframe(frame)
