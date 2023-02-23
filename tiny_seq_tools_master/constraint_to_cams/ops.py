import enum
import bpy
from bpy.utils import register_class, unregister_class
from tiny_seq_tools_master.constraint_to_cams.core import (
    set_rot_to_seq_cam,
    check_rot_to_cam_status,
    refresh_rot_to_cam_list,
)


class VIEW3D_OP_constraint_to_strip_camera(bpy.types.Operator):
    bl_idname = "object.rotate_to_strip_camera"
    bl_label = "Enable Rotate to Strip Cameras to Active"
    bl_description = "Enable Rotate to Strip Cameras to Active"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return not check_rot_to_cam_status(context.active_object)

    def execute(self, context):
        obj = context.active_object

        # check active object
        if obj is None:
            self.report({"ERROR"}, "There is no active object")
            return {"CANCELLED"}

        if obj.type == "CAMERA":
            self.report({"ERROR"}, "Cannot set 'Rotate to Strip Camera' on a Camera")
            return {"CANCELLED"}
        if obj.line_art_seq_obj:
            self.report(
                {"ERROR"},
                "Cannot set 'Rotate to Strip Camera' if 'Sequence Line Art' enabled",
            )
            return {"CANCELLED"}

        # remove if already on list
        rot_to_seq_cam_items = context.window_manager.rot_to_seq_cam_items
        for index, item in enumerate(rot_to_seq_cam_items):
            if item.object == obj:
                rot_to_seq_cam_items.remove(index)

        # clear any user create COPY ROTATION constaints
        if obj.constraints is not None:
            for constraint in obj.constraints:
                if constraint.type == "COPY_ROTATION":
                    obj.constraints.remove(constraint)

        set_rot_to_seq_cam(obj)

        # Add to list items
        add_rot_to_cam_item = rot_to_seq_cam_items.add()
        add_rot_to_cam_item.object = obj

        # Refresh UI
        context.scene.frame_set(int(context.scene.frame_current_final - 1))
        context.scene.frame_set(int(context.scene.frame_current_final + 1))
        self.report({"INFO"}, f"Added {obj.name} to Rotate to Constraint Items")
        return {"FINISHED"}


class VIEW3D_OP_constraint_to_strip_camera_remove(bpy.types.Operator):
    bl_idname = "object.remove_object_from_list"
    bl_label = "Disable Rotate to Strip Cameras from Active"
    bl_description = "Disable Rotate to Strip Cameras from Active"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return check_rot_to_cam_status(context.active_object)

    def execute(self, context):
        # Check for active object
        obj = context.active_object

        # Remove constraint
        for constraint in obj.constraints:
            if constraint.name == "ROT_TO_SEQ_CAM":
                obj.constraints.remove(constraint)

        # Remove from list of copy_rot_items
        rot_to_seq_cam_items = context.window_manager.rot_to_seq_cam_items
        for index, item in enumerate(rot_to_seq_cam_items):
            if item.object == obj:
                rot_to_seq_cam_items.remove(index)

        self.report({"INFO"}, f"Removed {obj.name} from Rotate to Constraint Items")
        return {"FINISHED"}


class VIEW3D_OP_refresh_copy_rot_items(bpy.types.Operator):
    bl_idname = "object.refresh_copy_rot_items"
    bl_label = "Refresh Rotate to Strip Cameras List"
    bl_description = "Refresh list of Rotate to Strip Cameras Items"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if not context.scene.sequence_editor:
            self.report({"ERROR"}, "There may be no edit in current scene")
            return {"CANCELLED"}
        scene_strips = [strip for strip in context.scene.sequence_editor.sequences_all if strip.type =="SCENE"]
        refresh_rot_to_cam_list(context, scene_strips)
        self.report({"INFO"}, "Strip Cameras List Updated")
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
