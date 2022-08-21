import bpy


def sync_update_line_art_objs(strip):
    if strip.id_data.line_art_cam_override:
        return
    for obj in strip.scene.objects:
        if obj.line_art_seq_cam is True:
            for mod in obj.grease_pencil_modifiers:
                if mod.type == "GP_LINEART":
                    mod.source_camera = strip.scene_camera


def check_animation_is_constant(line_art_mod):
    if line_art_mod.id_data.original.animation_data.action is None:
        return False
    for fcurve in line_art_mod.id_data.original.animation_data.action.fcurves:
        for kf in fcurve.keyframe_points:
            if kf.interpolation != "CONSTANT":
                return False
    return True


def check_keyframes_match_strip(obj, strip):
    if check_animation_is_constant(obj) == False:
        return False
    fcurves = obj.animation_data.action.fcurves
    keyframes = fcurves[0].keyframe_points
    keyframes = sorted(keyframes, key=lambda i: i.co[0], reverse=False)
    for key in keyframes:
        if key.co[0] in range(strip.frame_final_start, strip.frame_final_end):
            if key.co[0] != strip.frame_final_start:
                return False
    return True


def sync_seq_line_art(context, line_art_mod):
    for strip in context.scene.sequence_editor.sequences_all:
        line_art_mod.keyframe_insert("thickness", frame=strip.frame_final_start)

    for fcurve in line_art_mod.id_data.original.animation_data.action.fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = "CONSTANT"
