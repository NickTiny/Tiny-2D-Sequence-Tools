from tiny_seq_tools_master.rig_tools.rig_editor.tiny_media_data import (
    bools_to_add,
    tiny_media_bones_legend,
    bone_groups,
    tiny_media_bone_groups,
    tiny_lw_bones,
    tiny_hand_foot_bones,
)
from tiny_seq_tools_master.core_functions.object import (
    check_object_type,
    get_consts_on_obj,
)
from tiny_seq_tools_master.core_functions.drivers import add_driver, get_driver_ob_obj
from tiny_seq_tools_master.rig_tools.rig_editor.core import (
    get_action_offset_bones,
    get_action_from_constraints,
    hide_grease_pencil_editor,
    enable_all_mod_const,
    armature_bones_rename,
    bone_custom_prop_bools_add,
    bone_create_groups,
    bone_assign_groups,
    bone_ik_driver_add,
    bone_transform_mirror_add,
    bone_transform_nudge_add,
    bone_copy_location_nudge,
    bone_copy_location_limb,
    bone_ik_constraint_add,
    bone_position_limits_add,
    bone_check_constraint,
    bone_copy_transforms_add,
    bone_copy_location_add,
    add_ik_flip_to_pole,
    get_nudge_bone_name,
    copy_ik_rotation,
)
from tiny_seq_tools_master.core_functions.bone import (
    apply_transforms_on_frame,
    get_consts_on_bone,
    reset_bones,
    show_hide_constraints,
    add_action_const_to_head,
    add_action_const_to_body,
    bone_new,
    child_bone_new,
    child_bone_connected_new,
    calculate_bone_vector,
    make_limb_set,
    make_ik_bones
)
import bpy


# Imports data that should be read from a JSON file or other imported text format.

class RIGTOOLS_OT_create_armatue(bpy.types.Operator):
    bl_idname = "rigools.create_2d_armature"
    bl_label = "Create Armature"
    bl_description = "add better description."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return (not context.scene.target_armature)

    def execute(self, context):
        bpy.ops.object.armature_add(enter_editmode=True)
        # must be in edit mode to add bones
        arm_obj = context.active_object

        edit_bones = arm_obj.data.edit_bones

        # Clear Existing Bone
        for bone in edit_bones:
            edit_bones.remove(bone)

        # Create root bones
        master_bone = bone_new(
            edit_bones, 'Global.Location', (-.3, -.5), (.3, -.5))
        # Create Spine Bones
        spine_root = (0, .8)
        spine_root = child_bone_new(
            master_bone, 'Location', spine_root, calculate_bone_vector(.3, spine_root))
        lower_offset = (spine_root.tail.xz[0], (spine_root.tail.xz[1]+.1))
        lower = child_bone_new(
            spine_root, 'Lower', lower_offset, calculate_bone_vector(.7, lower_offset))
        upper = child_bone_connected_new(
            lower, 'Upper', calculate_bone_vector(.7, lower.tail.xz))
        neck = child_bone_new(upper, 'Neck', upper.tail.xz,
                              calculate_bone_vector(.2, upper.tail.xz))

        make_limb_set(parent=upper, limb='Arm', origin=(0.5, 2.5), angle=130,
                      appendage_angle=130, use_make_nudge=True, make_ik_bones=True)
        make_limb_set(lower, 'Leg', (.2, 1.4), 180, 180-45, True, True)

        # Select all bones to recalculate roll
        for bone in edit_bones:
            bone.select = True
        bpy.ops.armature.calculate_roll(
            type='GLOBAL_POS_Y', axis_flip=False, axis_only=False)
        bpy.ops.object.mode_set(mode='POSE')
        #bpy.context.view_layer.update()
        context.scene.target_armature = arm_obj
        
        self.report({"INFO"}, "Created Armature")
        return {"FINISHED"}


class RIGTOOLS_rig_edit_base_class(bpy.types.Operator):
    """Base Class for all Rig Edit Operations"""

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        res = not (obj.library or obj.override_library)
        if not res:
            cls.poll_message_set("Cannot Edit Reference Objects")
        return res


class RIGTOOLS_enter_grease_pencil_editor(bpy.types.Operator):
    bl_idname = "rigools.enter_grease_pencil_editor"
    bl_label = "Edit Selected Grease Pencil"
    bl_description = "Edit Selected Grease Pencil"
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        res = not (
            obj.library
            or obj.override_library
           # or context.window_manager.gpencil_editor_active
        )
        if not res:
            cls.poll_message_set("Cannot Edit Reference Objects")
        return res

    def execute(self, context):
        obj = context.active_object
        obj_type = "GPENCIL"
        if not check_object_type(obj, obj_type):
            self.report({"ERROR"}, f"Active Object type must be {obj_type}")
            return {"CANCELLED"}
        if hide_grease_pencil_editor(obj, False) is False:
            self.report({"ERROR"}, f"{obj.name} failed to enter draw mode")
            return {"CANCELLED"}
        context.window_manager.gpencil_editor_active = obj.data
        self.report({"INFO"}, f"{obj.name} entered draw mode")
        return {"FINISHED"}


class RIGTOOLS_enter_grease_pencil_editor_exit(RIGTOOLS_rig_edit_base_class):
    bl_idname = "rigools.enter_grease_pencil_editor_exit"
    bl_label = "Exit Edit Selected Grease Pencil"
    bl_description = "Exit Edit on Selected Grease Pencil"
    bl_options = {"UNDO"}

    def execute(self, context):
        obj = context.active_object
        obj_type = "GPENCIL"
        if not check_object_type(obj, obj_type):
            self.report({"ERROR"}, f"Active Object type must be {obj_type}")
            return {"CANCELLED"}
        if hide_grease_pencil_editor(obj, True) is False:
            self.report({"ERROR"}, f"{obj.name} failed to enter draw mode")
            return {"CANCELLED"}
        context.window_manager.gpencil_editor_active = None
        self.report({"INFO"}, f"{obj.name} exited draw mode")
        return {"FINISHED"}


class RIGTOOLS_isolate_gpencil(bpy.types.Operator):
    bl_idname = "rigools.isolate_gpencil"
    bl_label = "Isolate Selected Grease Pencil"
    bl_description = "Toggles Isolation for objects in the current scene"
    bl_options = {"UNDO"}

    def execute(self, context):
        bpy.ops.view3d.localview(frame_selected=True)
        return {"FINISHED"}


class RIGTOOLS_enable_all_gp_mod_const(bpy.types.Operator):
    bl_idname = "rigools.enable_all_gp_mod_const"
    bl_label = "Check all Grease Pencil Objects"
    bl_description = "Ensure all Grease Pencil Modifiers are enabled if any are not."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        enable_all_mod_const(context.active_object, True)
        self.report({"INFO"}, "All Modifiers and Constraints are Enabled!")
        return {"FINISHED"}


old_action = None


class RIGTOOLS_initialize_rig(bpy.types.Operator):
    bl_idname = "rigools.initialize_rig"
    bl_label = "Initialize Rig"
    bl_description = "Load all of the rig settings"
    bl_options = {"REGISTER", "UNDO"}

    pose_length_set: bpy.props.IntProperty(name="Turnaround Length")
    update_face_constraints: bpy.props.BoolProperty(
        name="Add Face Constraints", default=False)
    set_turnaround: bpy.props.BoolProperty(
        name="Turnaround", default=False)

    @classmethod
    def poll(cls, context):
        return     context.scene.bone_selection



    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        col = self.layout.column(align=True)

        col.prop(self, "update_face_constraints")
        col.prop(self, "is_turnaround")
        if self.set_turnaround:
            col = self.layout.column()
            col.label(text="Proceed with Caution!", icon="ERROR")

            lines = [
                "Turnaround Length effects how the turnaround pose ",
                "is interperted. Changing this will break compatibility",
                "with previous animations tracks.",
            ]
            for line in lines:
                col.alert = True
                col.label(text=line)
            col.label(text="Use 'ESC' to cancel")
            if context.active_object.tiny_rig.pose_length:
                self.pose_length_set = context.active_object.tiny_rig.pose_length
            col.prop(self, "pose_length_set")

    def execute(self, context):
        # TODO Make safe to re-run (collect related bones clear and reset)
        msg = ""
        obj = context.active_object
        if context.scene.bone_selection is None:
            self.report({"ERROR"}, f"Set Property Bone")
            return {"CANCELLED"}
        propbone = obj.pose.bones[context.scene.bone_selection]

        bpy.ops.object.mode_set(mode='EDIT')
        for hand_bone in [bone for bone in obj.data.edit_bones if bone.name in tiny_hand_foot_bones]:
            hand_bone.parent = None
            hand_bone.select = True

        for bone in [bone for bone in obj.data.edit_bones if bone.name in tiny_lw_bones]:
            prefix = bone.name[0]
            limb = bone.name[2:5]
            make_ik_bones(obj.data.edit_bones[f"{prefix}_{limb}_Nudge"], bone)

        bpy.ops.object.mode_set(mode='POSE')

        # Set as Rig
        obj.tiny_rig.is_rig = True

        # Set bone for poperties
        obj.tiny_rig.pose_data_name = context.scene.bone_selection

        # Set Turnaround Length
        if self.set_turnaround:
            obj.tiny_rig.pose_length = self.pose_length_set
            msg += (f"Pose Length set to {obj.tiny_rig.pose_length} \n")

        bone_groups_created = bone_create_groups(obj, bone_groups)
        if bone_groups_created:
            msg += (f"Bones Group Created \n")

        updated_bones = bone_assign_groups(obj, tiny_media_bone_groups)
        msg += (f"{updated_bones} \n")

        # Add Driver Properties
        # TODO only add relavant bools
        bone_custom_prop_bools_add(propbone, bools_to_add)

        # TODO only clear constraitns for needed bones
        for bone in [bone for bone in obj.pose.bones if bone.constraints]:
            for constraint in bone.constraints:
                bone.constraints.remove(constraint)

        # TODO LOCK ALL BONES TO SINGLE AXIS
        for bone in obj.pose.bones:
            bone.rotation_mode = 'XYZ'
            bone.lock_rotation[0] = True
            bone.lock_rotation[1] = True
            bone.lock_rotation[2] = False
            bone.rotation_mode = 'XYZ'
            bone.lock_rotation[0] = False
            bone.lock_rotation[1] = False
            bone.lock_location[2] = True

        # Add IK Constraints
        ik_bones = [
            bone for bone in obj.pose.bones if bone.name in tiny_lw_bones]
        for bone in ik_bones:
            if not get_consts_on_bone(bone, "IK"):
                prefix = bone.name[0]
                suffix = bone.name[2:5]
                bone_ik_constraint_add(bone, prefix, suffix)
                msg += (f"IK Added on '{bone.name}'/n")
            constraint = get_consts_on_bone(bone, "IK")[0]
            # Must be exactly on IK modifier
            if len(get_consts_on_bone(bone, "IK")) != 1:
                self.report({"ERROR"}, f"Too many IKs on {bone.name}")
                return {"CANCELLED"}
            # Add IK Drivers
            bone_ik_driver_add(bone, constraint, propbone,
                               f"{bone.name.split('.')[0]}_IK")

        # Add IK_Flip to Poles
        for bone in [bone for bone in obj.pose.bones if "Pole" in bone.name]:
            # If nudge pass the corrisponding nudge bone, else pass master bone
            nudge_bone_name = get_nudge_bone_name(bone)
            prefix = bone.name[0]
            suffix = bone.name[2:5]
            ik_prop_name = f"{prefix}_{suffix}_Flip_IK"

            constraint = add_ik_flip_to_pole(bone, nudge_bone_name)
            add_driver(
                bone.id_data,
                bone.id_data,
                ik_prop_name,
                f'pose.bones["{bone.name}"].constraints["{constraint.name}"].influence',
                f'pose.bones["{propbone.name}"]["{ik_prop_name}"]',
                -1,
            )
            # Nudge with special conditions

            bone_copy_location_nudge(bone, 'LOCAL', True)

        # Add Mirror to Hand/Foot Bones
        for bone in [bone for bone in obj.pose.bones if bone.name in tiny_hand_foot_bones]:
            bone_copy_location_nudge(bone, 'POSE', True)
            bone_copy_location_limb(context, bone, False)
            prefix = bone.name[0]
            suffix = bone.name[2:5]
            target_name = f"{prefix}_{suffix}_IK"
            copy_ik_rotation(bone, target_name)
            bone_transform_mirror_add(bone)

        # Add Hand Nudge
        for bone in [bone for bone in obj.pose.bones if "Hand" in bone.name]:
            if not bone_check_constraint(bone, "HAND_NUDGE"):
                bone_transform_nudge_add(bone)
                msg += (f"Nudge Const Added on '{bone.name}'\n")

        # Add Position Limits
        for bone in [bone for bone in obj.pose.bones if "Nudge" in bone.name]:
            if not bone_check_constraint(bone, "Nudge - Limit Location"):
                bone_position_limits_add(bone)
                msg += (f"Position Limits Added on '{bone.name}'\n")

        # IK Ctrl Copy Transforms
        for bone in [bone for bone in obj.pose.bones if "IK" in bone.name]:
            if not bone_check_constraint(bone, "Copy Arm Location"):
                bone_copy_location_limb(context, bone)
                msg += (f"Copy Arm Loc Added on '{bone.name}'\n")
            if not bone_check_constraint(bone, "Copy Nudge Location"):
                bone_copy_location_nudge(bone)
                msg += (f"Copy Nudge Loc Added on '{bone.name}'\n")

        # add turnaround action
        if obj.offset_action is None:
            action = bpy.data.actions.new(f'{obj.name}_TURNAROUND')
            obj.offset_action = action

        # if self.update_face_constraints:
        #     # Copy Face Rig Transforms
        #     # Eyebrows
        #     for bone in [bone for bone in obj.pose.bones if "Eyebrow" in bone.name]:
        #         name = "COPY_FACE_RIG"
        #         if ".001" not in bone.name:
        #             if not bone_check_constraint(bone, name):
        #                 bone_copy_transforms_add(bone, name)
        #                 msg += (f"{name} added to '{bone.name}'\n")

        #     # Eyelids
        #     for bone in [bone for bone in obj.pose.bones if "Eyelid" in bone.name]:
        #         name = "COPY_FACE_RIG"
        #         if ".001" not in bone.name:
        #             if not bone_check_constraint(bone, name):
        #                 bone_copy_transforms_add(bone, name)
        #                 msg += (f"{name} added to '{bone.name}'\n")

        #     # Eyes
        #     for bone in [bone for bone in obj.pose.bones if bone.name == "Eye.R.M" or bone.name == "Eye.L.M"]:
        #         name = "COPY_EYE_AIM"
        #         if not bone_check_constraint(bone, name):
        #             bone_copy_location_add(bone, f"Eye_Aim", False, name)
        #             msg += (f"{name} added to '{bone.name}'\n")
        #         name = "COPY_EYE_CTRL"
        #         if not bone_check_constraint(bone, name):
        #             bone_copy_location_add(bone, f"{bone.name.split('.M')[0]}.ctrl", True, name)
        #             msg += (f"{name} added to '{bone.name}'\n")
        # Select all bones to recalculate roll

        bpy.ops.object.mode_set(mode='EDIT')
        for bone in obj.data.edit_bones:
            bone.select = True
        bpy.ops.armature.calculate_roll(
            type='GLOBAL_POS_Y', axis_flip=False, axis_only=False)
        bpy.ops.object.mode_set(mode='POSE')

        self.report({"INFO"}, f"Initilizaton Completed! \n {msg}")
        return {"FINISHED"}


class RIGTOOLS_toggle_enable_action(bpy.types.Operator):
    @classmethod
    def poll(cls, context):
        if not context.active_object.animation_data:
            return False
        return (
            context.active_object.animation_data.action
            != context.active_object.offset_action
            and context.active_object.mode == "POSE"
        )

    bl_idname = "rigools.enable_offset_action"
    bl_label = "Edit Offset Action"
    bl_description = "Enable Turnaround Offset Action Editor"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object

        if context.window_manager.offset_editor_active == True:
            self.report({"ERROR"}, "Offset Editor already Enabled")
            return {"CANCELLED"}
        offset_action = obj.offset_action
        if not offset_action:
            self.report({"ERROR"}, "Offset Action not Set")
            return {"CANCELLED"}
        if obj.mode != "POSE":
            self.report({"ERROR"}, "Must be in POSE Mode")
            return {"CANCELLED"}
        if obj.animation_data.action == offset_action:
            self.report({"ERROR"}, "Offset Action already Enabled")
            return {"CANCELLED"}
        if obj.animation_data and obj.animation_data.action:
            global old_action
            old_action = obj.animation_data.action

        obj.animation_data.action = None
        reset_bones(obj.pose.bones)
        constraints = get_action_offset_bones(obj.pose.bones)
        show_hide_constraints(constraints, False)
        obj.animation_data.action = offset_action
        context.window_manager.offset_editor_active = True
        self.report({"INFO"}, "Offset Editing Enabled!")
        return {"FINISHED"}


class RIGTOOLS_toggle_disable_action(RIGTOOLS_rig_edit_base_class):
    bl_idname = "rigools.disable_offset_action"
    bl_label = "Disable Offset Action Editing"
    bl_description = "Disable Turnaround Offset Action Editor"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return (
            context.active_object.animation_data.action
            == context.active_object.offset_action
            and context.active_object.mode == "POSE"
        )

    def execute(self, context):
        obj = context.active_object
        offset_action = obj.offset_action
        if not offset_action:
            self.report({"ERROR"}, "Offset Action not Set")
            return {"CANCELLED"}
        if not obj.animation_data.action == offset_action:
            self.report({"ERROR"}, "Offset Action not Enabled")
            return {"CANCELLED"}
        obj.animation_data.action = None
        reset_bones(obj.pose.bones)
        constraints = get_action_offset_bones(obj.pose.bones)
        show_hide_constraints(constraints, True)
        context.window_manager.offset_editor_active = False
        global old_action
        if old_action is not None:
            obj.animation_data.action = old_action
        self.report({"INFO"}, "Offset Editing Disabled!")
        return {"FINISHED"}


class RIGTOOLS_load_action(RIGTOOLS_rig_edit_base_class):
    bl_idname = "rigools.load_action"
    bl_label = "Load Offset Action"
    bl_description = "Offset Action"
    bl_options = {"UNDO"}

    def execute(self, context):
        offset_action = get_action_from_constraints(
            context.active_object.pose.bones)
        context.active_object.offset_action = offset_action
        return {"FINISHED"}


class RIGTOOLS_add_action_const_to_bone(bpy.types.Operator):
    bl_idname = "rigools.add_action_const_to_bone"
    bl_label = "Add Offset to Selected Bones"
    bl_description = """If a bone is included in the active_object's 'Offset Action' add constraint to move bone via action constraint. 
    This will also add a driver back to the Body/Head Poses"""
    bl_options = {"UNDO"}

    is_head: bpy.props.BoolProperty(
        name="Is Head",
        description="Set selected bone(s) as Head Turnaround and create a Head Pose Action Offset. Else Body Action Offset",
    )

    @classmethod
    def poll(cls, context):
        obj = context.scene.target_armature
        res = not (
            obj.library
            or obj.override_library
            or obj.animation_data.action == obj.offset_action
        )
        if not res:
            cls.poll_message_set(
                "Cannot Edit while Offsetting Turnaround Action")
        return res

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        self.layout.prop(self, "is_head")

    def execute(self, context):
        if self.is_head:
            add_action_const_to_head(context)
        else:
            add_action_const_to_body(context)
        return {"FINISHED"}


class RIGTOOLS_add_ik_mirror_to_pole(RIGTOOLS_rig_edit_base_class):
    bl_idname = "rigools.add_ik_mirror_to_pole"
    bl_label = "Add Flip to Pole Bone"
    bl_description = """Add Mirror Pole Transform Constraint to selected Bone"""
    bl_options = {"UNDO"}

    def execute(self, context):
        bone = context.active_pose_bone
        if "_Pole" not in bone.name:
            self.report({"ERROR"}, f"Active Bone must be Pole Target")
            return {"CANCELLED"}

        suffix = bone.name.split("_Pole")[0]
        if not get_consts_on_bone(bone, "TRANSFORM"):
            new = bone.constraints.new("TRANSFORM")
            new.target = context.active_object
            new.subtarget = f"{suffix}_Nudge"
            new.target_space = "LOCAL_WITH_PARENT"
            new.owner_space = "LOCAL_WITH_PARENT"
            new.to_min_y = -4.5
            add_driver(
                bone.id_data,
                bone.id_data,
                f"{suffix}_Flip_IK",
                f'pose.bones["{bone.name}"].constraints["{new.name}"].influence',
                f'pose.bones["{bone.id_data.tiny_rig.pose_data_name}"]["{suffix}_Flip_IK"]',
            )

        return {"FINISHED"}


class RIGTOOLS_add_hand_nudge(RIGTOOLS_rig_edit_base_class):
    bl_idname = "rigools.add_hand_nudge"
    bl_label = "Add Nudge to Hand Bone"
    bl_description = """Add Hand Nudge Constraint to selected Bone"""
    bl_options = {"UNDO"}

    def execute(self, context):

        bone = context.active_pose_bone
        if "_Arm.Hand" not in bone.name:
            self.report({"ERROR"}, f"Active Bone must be Hand")
            return {"CANCELLED"}
        if "HAND_NUDGE" in [const.name for const in bone.constraints]:
            self.report(
                {"ERROR"}, f"Hand Nundge already exists on {bone.name}")
            return {"CANCELLED"}

        bone_transform_nudge_add(bone)
        return {"FINISHED"}


class RIGTOOLS_add_nudge_position_limits(RIGTOOLS_rig_edit_base_class):
    bl_idname = "rigools.add_nudge_position_limits"
    bl_label = "Add Position Limits"
    bl_description = """Add Position Nudge Constraint to selected Bone"""
    bl_options = {"UNDO"}

    def execute(self, context):
        mod_name = "Nudge - Limit Location"
        bone = context.active_pose_bone
        if "Nudge" not in bone.name:
            self.report({"ERROR"}, f"Active Bone must be Nudge")
            return {"CANCELLED"}
        if mod_name in [const.name for const in bone.constraints]:
            self.report(
                {"ERROR"}, f"Hand Nundge already exists on {bone.name}")
            return {"CANCELLED"}

        suffix = bone.name.split(".Hand")[0]
        side = suffix.split("_Arm")[0]
        new = bone.constraints.new("LIMIT_LOCATION")
        new.owner_space = "LOCAL"
        new.use_min_z = True
        new.use_max_z = True
        new.min_z = -0.1
        new.max_z = 0.1
        new.name = mod_name
        return {"FINISHED"}


class RIGTOOLS_add_mirror_to_bone(RIGTOOLS_rig_edit_base_class):
    bl_idname = "rigools.add_mirror_to_hand_foot_bone"
    bl_label = "Add Flip to Hand/Foot Bone"
    bl_description = """Add Hand Foot Mirror+CopyTra"""
    bl_options = {"UNDO"}

    def execute(self, context):
        bone = context.active_pose_bone
        if not (".Hand" in bone.name or ".Foot" in bone.name):
            self.report({"ERROR"}, f"Active Bone must be Hand or Foot")
            return {"CANCELLED"}
        if "FLIP_BONE" in [const.name for const in bone.constraints]:
            self.report(
                {"ERROR"}, f"Hand Nundge already exists on {bone.name}")
            return {"CANCELLED"}

        bone_transform_mirror_add(bone)
        return {"FINISHED"}


class RIGTOOLS_add_copy_transforms_to_ik_ctrl(RIGTOOLS_rig_edit_base_class):
    bl_idname = "rigools.add_copy_transforms_to_ik_ctrl"
    bl_label = "Add Copy Transforms to Hand/Foot Bone"
    bl_description = """Add Hand Foot Mirror+CopyTra"""
    bl_options = {"UNDO"}

    def execute(self, context):
        bone = context.active_pose_bone
        bone_copy_location_limb(context, bone)
        bone_copy_location_nudge(bone)

        return {"FINISHED"}


class RIGTOOLS_apply_legacy_transforms(RIGTOOLS_rig_edit_base_class):
    bl_idname = "rigtools.apply_legacy_transforms"
    bl_label = "Apply Legacy Constraints on Current Frame"
    bl_description = (
        """Apply Legacy Transform Constraints on Current Frame for selected bones"""
    )
    bl_options = {"UNDO"}

    def execute(self, context):
        apply_transforms_on_frame(
            context.scene.frame_current, context.selected_pose_bones
        )
        return {"FINISHED"}


class RIGTOOLS_add_ik_fk_toggle(RIGTOOLS_rig_edit_base_class):
    bl_idname = "rigtools.add_ik_fk_toggle"
    bl_label = "Add IK Toggle"
    bl_description = """Add Prop to Posebone, drive influence of IK constraint and Copy Rotation of hand."""
    bl_options = {"UNDO"}

    def execute(self, context):
        # From selected IK Bone
        bone = context.active_pose_bone
        propbone = context.active_object.pose.bones[context.scene.bone_selection]
        constraint = None
        for const in bone.constraints:
            if const.type == "IK":
                constraint = const

        if constraint is None:
            self.report({"ERROR"}, f"Active Bone must have IK")
            return {"CANCELLED"}

        bone_ik_driver_add(bone, constraint, propbone,
                           f"{bone.name.split('.')[0]}_IK")
        return {"FINISHED"}


class RIGTOOLS_add_custom_prop(RIGTOOLS_rig_edit_base_class):
    bl_idname = "rigools.add_custom_prop"
    bl_label = "Add Custom Props"
    bl_description = """TODO"""
    bl_options = {"UNDO"}

    def execute(self, context):
        obj = context.active_object
        prop_bone = obj.pose.bones[context.scene.bone_selection]
        for bone in obj.pose.bones:
            bone.bone.select = False
        prop_bone.bone.select = True
        bpy.ops.wm.properties_add(data_path="active_pose_bone")
        return {"FINISHED"}


class RIGTOOLS_gp_constraint_armature(bpy.types.Operator):
    bl_idname = "rigools.gp_constraint_armature"
    bl_label = "Add Armature Contraint"
    bl_description = """"""  # TODO
    bl_options = {"UNDO"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        self.layout.prop(context.scene, "target_bone")
        

    @classmethod
    def poll(cls, context):
        return (context.active_object.type == "GPENCIL")

    def execute(self, context):
        obj = context.active_object
        const = obj.constraints.new("ARMATURE")
        const.name = "ARMATURE_CONST"
        const.targets.new()
        target_entry = const.targets[-1]
        target_entry.target= context.scene.target_armature
        target_entry.subtarget = context.scene.target_bone
        return {"FINISHED"}

class RIGTOOLS_gp_vertex_by_layer(bpy.types.Operator):
    bl_idname = "rigools.gp_vertex_by_layer"
    bl_label = "Vertex Parent Active Layer"
    bl_description = """"""  # TODO
    bl_options = {"UNDO"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        self.layout.prop(context.scene, "target_bone")
    
    def get_frames(self, context, gp_layer):
        return [frame.frame_number for frame in gp_layer.frames]  
    
    def get_vertex_group(self, object, name):
        # try:
        group = object.vertex_groups.get(f'{name}')
        if not group:
            object.vertex_groups.new(name=f'{name}')
            group = object.vertex_groups.get(f'{name}')
        return group.index
    def get_modifier(self, context):
        obj = context.active_object
        mod = obj.grease_pencil_modifiers.get("ARMATURE_MOD")
        if mod is None:
            mod = obj.grease_pencil_modifiers.new(name= "ARMATURE_MOD", type="GP_ARMATURE")
        return mod

    @classmethod
    def poll(cls, context):
        return (context.active_object.type == "GPENCIL" and context.scene.target_armature)

    def execute(self, context):
        obj = context.active_object
        layer = obj.data.layers.active
        mod = self.get_modifier(context)
        mod.object = context.scene.target_armature
        bpy.ops.object.mode_set(mode='EDIT_GPENCIL')
        bone = context.scene.target_armature.pose.bones[context.scene.target_bone]
        if bone is False:
            self.report({"ERROR"}, f"Bone not found")
            return {"CANCELLED"}
        for frame in self.get_frames(context, layer):
            context.scene.frame_set(frame)
            context.scene.tool_settings.gpencil_selectmode_edit = 'POINT'
            obj.vertex_groups.active_index = self.get_vertex_group(obj, bone.name)
            for other_layer in [pther_layer for pther_layer in obj.data.layers if pther_layer.info != layer.info]:
                other_layer.lock = True
            layer.lock = False
            bpy.ops.gpencil.select_all(action='SELECT')
            bpy.ops.gpencil.vertex_group_assign()
            bpy.ops.gpencil.select_all(action='DESELECT')
        return {"FINISHED"}

classes = (
    RIGTOOLS_OT_create_armatue,
    RIGTOOLS_add_ik_fk_toggle,
    RIGTOOLS_apply_legacy_transforms,
    RIGTOOLS_add_action_const_to_bone,
    RIGTOOLS_toggle_enable_action,
    RIGTOOLS_toggle_disable_action,
    RIGTOOLS_load_action,
    RIGTOOLS_initialize_rig,
    RIGTOOLS_add_ik_mirror_to_pole,
    RIGTOOLS_add_hand_nudge,
    RIGTOOLS_add_nudge_position_limits,
    RIGTOOLS_add_mirror_to_bone,
    RIGTOOLS_enter_grease_pencil_editor,
    RIGTOOLS_enter_grease_pencil_editor_exit,
    RIGTOOLS_isolate_gpencil,
    RIGTOOLS_enable_all_gp_mod_const,
    RIGTOOLS_add_custom_prop,
    RIGTOOLS_add_copy_transforms_to_ik_ctrl,
    RIGTOOLS_gp_constraint_armature,
    RIGTOOLS_gp_vertex_by_layer,
)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
