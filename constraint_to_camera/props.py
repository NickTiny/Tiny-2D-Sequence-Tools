import bpy
from bpy.utils import register_class, unregister_class


def enum_items_generator(self, context):
    scene = context.active_sequence_strip.scene
    enum_items = []
    for obj in scene.objects:
        for constraint in obj.constraints:
            if constraint.type == "COPY_ROTATION":
                enum_items.append(
                    (
                        str(constraint),
                        f"{constraint.id_data.name}",
                        f"{constraint.id_data.name} - {constraint.name}",
                    )
                )
    return enum_items


def get_rot_to_seq_cam_state(self):
    obj = self.id_data
    for constraint in obj.constraints:
        if constraint.type == "COPY_ROTATION":
            return True
    return False


def set_rot_to_seq_cam(self, value: bool):
    if not self:
        obj = self.id_data
        if obj.constraints is not None:
            for constraint in obj.constraints:
                if constraint.type == "COPY_ROTATION":
                    obj.constraints.remove(constraint)
        bpy.ops.object.constraint_add(type="COPY_ROTATION")
        for constraint in obj.constraints:
            if constraint.type == "COPY_ROTATION":
                constraint.use_x = False
                constraint.use_y = False
                constraint.use_z = True
        return True


def get_line_art_seq_cam_state(self):
    obj = self
    if obj.grease_pencil_modifiers is None:
        return False
    for mod in obj.grease_pencil_modifiers:
        if mod.type == "GP_LINEART":
            if mod.use_custom_camera is True:
                return True
    return False


def set_line_art_seq_cam_state(self, value: bool):
    if not self:
        obj = self
        for mod in obj.grease_pencil_modifiers:
            if mod.type == "GP_LINEART":
                if mod.use_custom_camera:
                    return True
        return


class constraint_to_camera_items(bpy.types.PropertyGroup):
    avaliable_properties: bpy.props.EnumProperty(
        items=enum_items_generator, name="Objects Rotated to Camera"
    )


classes = (constraint_to_camera_items,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.constraint_camera = bpy.props.PointerProperty(
        type=constraint_to_camera_items
    )
    bpy.types.Object.rot_to_seq_cam = bpy.props.BoolProperty(
        name="Enable Rotate to Strip Cameras",
        default=False,
        get=get_rot_to_seq_cam_state,
        set=set_rot_to_seq_cam,
        options=set(),
    )
    bpy.types.Object.line_art_seq_cam = bpy.props.BoolProperty(
        name="Enable Seq Line Art Control",
        default=False,
        get=get_line_art_seq_cam_state,
        set=set_line_art_seq_cam_state,
        options=set(),
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
