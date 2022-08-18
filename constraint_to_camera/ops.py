import bpy
from bpy.utils import register_class, unregister_class


class VIEW3D_OP_constraint_to_strip_camera(bpy.types.Operator):
    bl_idname = "object.rotate_to_strip_camera"
    bl_label = "Enable Rotate to Strip Cameras to Active"

    def execute(self, context):
        obj = context.active_object
        if obj is None:
            self.report({"ERROR"}, "There is no active object")
            return {"CANCELLED"}
        if obj.constraints is not None:
            for constraint in obj.constraints:
                if constraint.type == "COPY_ROTATION":
                    obj.constraints.remove(constraint)
        window = context.window_manager.windows[0]
        with context.temp_override(window=window):
            bpy.ops.object.constraint_add(type="COPY_ROTATION")
        for constraint in obj.constraints:
            if constraint.type == "COPY_ROTATION":
                constraint.use_x = False
                constraint.use_y = False
                constraint.use_z = True
        obj.rot_to_seq_cam = True
        context.scene.frame_set(int(context.scene.frame_current_final - 1))
        context.scene.frame_set(int(context.scene.frame_current_final + 1))
        return {"FINISHED"}


class VIEW3D_OP_constraint_to_strip_camera_remove(bpy.types.Operator):
    bl_idname = "object.remove_object_from_list"
    bl_label = "Disable Rotate to Strip Cameras from Active"

    def execute(self, context):
        obj = context.active_object
        if obj is None:
            self.report({"ERROR"}, "There is no active object")
            return {"CANCELLED"}
        rot_to_seq_cam = context.active_object.rot_to_seq_cam
        if rot_to_seq_cam is None:
            self.report({"ERROR"}, "Active Object is Not Rotated to Camera")
            return {"CANCELLED"}
        rot_to_seq_cam = False
        for obj in context.scene.objects:
            for constraint in obj.constraints:
                if constraint.type == "COPY_ROTATION":
                    obj.constraints.remove(constraint)

        return {"FINISHED"}


classes = (
    VIEW3D_OP_constraint_to_strip_camera_remove,
    VIEW3D_OP_constraint_to_strip_camera,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
