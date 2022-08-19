import bpy
from operator import attrgetter
from bpy.utils import register_class, unregister_class


OldStrip = ""


# def update_line_art_objs(strip):
#     for obj in strip.scene.objects:
#         if obj.line_art_seq_cam is True:
#             for mod in obj.grease_pencil_modifiers:
#                 if mod.type == "GP_LINEART":
#                     mod.source_camera = strip.scene_camera


def constraint_to_active_camera(strip: bpy.types.Sequence):
    for item in bpy.data.window_managers[0].rot_to_seq_cam_items:
        obj = item.object
        for constraint in obj.constraints:
            if constraint.type == "COPY_ROTATION":
                constraint.target = strip.scene_camera


def update_constraint_camera(scene):
    global OldStrip
    scn = scene
    seq = scn.sequence_editor.sequences
    seq = sorted(seq, key=attrgetter("channel", "frame_final_start"))
    cf = scn.frame_current
    for i in seq:
        try:
            if i.type == "SCENE" and i.name != OldStrip:
                if i.frame_final_start <= cf and i.frame_final_end > cf and not i.mute:
                    constraint_to_active_camera(i)
                    # update_line_art_objs(i)
                    break
        except AttributeError:
            pass


@bpy.app.handlers.persistent
def constraint_to_camera_handler(self, context):
    update_constraint_camera(self)


classes = ()


def register():
    bpy.app.handlers.frame_change_pre.append(constraint_to_camera_handler)


def unregister():
    bpy.app.handlers.frame_change_pre.remove(constraint_to_camera_handler)
