import enum
import bpy
from bpy.utils import register_class, unregister_class


class VIEW3D_OP_constraint_to_strip_camera(bpy.types.Operator):
    bl_idname = "object.rotate_to_strip_camera"
    bl_label = "Enable Rotate to Strip Cameras to Active"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return context.active_object and not context.active_object.rot_to_seq_cam

    def execute(self, context):
        obj = context.active_object
        if obj is None:
            self.report({"ERROR"}, "There is no active object")
            return {"CANCELLED"}

        # remove if already on list
        rot_to_seq_cam_items = context.scene.rot_to_seq_cam_items
        for index, item in enumerate(rot_to_seq_cam_items):
            if item.object == obj:
                rot_to_seq_cam_items.remove(index)

        # clear any user create COPY ROTATION constaints
        if obj.constraints is not None:
            for constraint in obj.constraints:
                if constraint.type == "COPY_ROTATION":
                    obj.constraints.remove(constraint)

        # add new rotation constraint
        window = context.window_manager.windows[0]
        with context.temp_override(window=window):
            bpy.ops.object.constraint_add(type="COPY_ROTATION")

        # loop through constraints incase user has other constraints
        for constraint in obj.constraints:
            if constraint.type == "COPY_ROTATION":
                constraint.use_x = False
                constraint.use_y = False
                constraint.use_z = True
                obj.rot_to_seq_cam = True

        # Add to list items
        add_rot_to_cam_item = rot_to_seq_cam_items.add()
        add_rot_to_cam_item.object = obj

        context.scene.frame_set(int(context.scene.frame_current_final - 1))
        context.scene.frame_set(int(context.scene.frame_current_final + 1))
        return {"FINISHED"}


class VIEW3D_OP_constraint_to_strip_camera_remove(bpy.types.Operator):
    bl_idname = "object.remove_object_from_list"
    bl_label = "Disable Rotate to Strip Cameras from Active"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return context.active_object and context.active_object.rot_to_seq_cam

    def execute(self, context):
        # Check for active object
        obj = context.active_object

        # Check for active strip
        rot_to_seq_cam = context.active_object.rot_to_seq_cam
        if rot_to_seq_cam is None:
            self.report({"ERROR"}, "Active Object is Not Rotated to Camera")
            return {"CANCELLED"}

        # Remove constraint
        for constraint in obj.constraints:
            if constraint.type == "COPY_ROTATION":
                obj.constraints.remove(constraint)

        # Remove from list of copy_rot_items
        rot_to_seq_cam_items = context.scene.rot_to_seq_cam_items
        for index, item in enumerate(rot_to_seq_cam_items):
            if item.object == obj:
                rot_to_seq_cam_items.remove(index)

        # Set avaliablity to false
        rot_to_seq_cam = False

        return {"FINISHED"}


class VIEW3D_OP_refresh_copy_rot_items(bpy.types.Operator):
    bl_idname = "object.refresh_copy_rot_items"
    bl_label = "Refresh Rotate to Strip Cameras List"

    def execute(self, context):
        strip = context.active_sequence_strip
        rot_to_seq_cam_items = context.scene.rot_to_seq_cam_items
        rot_to_seq_cam_items.clear()
        if strip is None or strip.type != "SCENE":
            self.report({"ERROR"}, "There is no active scene strip")
            return {"CANCELLED"}
        for obj in strip.scene.objects:
            if obj.rot_to_seq_cam:
                for constraint in obj.constraints:
                    if constraint.type == "COPY_ROTATION":
                        add_rot_to_cam_item = rot_to_seq_cam_items.add()
                        add_rot_to_cam_item.object = obj

        return {"FINISHED"}


classes = (
    VIEW3D_OP_constraint_to_strip_camera_remove,
    VIEW3D_OP_constraint_to_strip_camera,
    VIEW3D_OP_refresh_copy_rot_items,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
