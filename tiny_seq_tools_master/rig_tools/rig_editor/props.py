import bpy

classes = ()

def bone_groups(self, context):
    bone_groups = context.scene.target_armature.pose.bone_groups
    items = []
    for bone_group in bone_groups:
          items.append((bone_group.name, bone_group.name, ""))
    items.append(("All_Bones", "All Bones", ""))
    return items


def get_user_props(self, context):
    items = []
    obj = context.scene.target_armature
    bone = obj.pose.bones[context.scene.property_bone_name]
    for x in bone.keys():
        if (x in obj.tiny_rig.user_props):
            items.append((f'{x}', f'{x}', f'{x}'))
    return items


def find_bones(self, context):
    return context.scene.target_armature.pose.bones


def check_armature(self, object):
    return object.type == "ARMATURE"


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.target_armature = bpy.props.PointerProperty(
        name="Target Arm", type=bpy.types.Object, poll=check_armature)
    bpy.types.WindowManager.offset_editor_active = bpy.props.BoolProperty(
        name="Offset Editor is Active", default=False
    )
    bpy.types.WindowManager.gpencil_editor = bpy.props.PointerProperty(
        type=bpy.types.Object, name="Active Object", description="Name of Active Grease Pencil Object"
    )

    bpy.types.Scene.target_bone_group = bpy.props.EnumProperty(
        name="Bone Group", items=bone_groups,)
    bpy.types.Scene.target_user_prop = bpy.props.EnumProperty(
        name="User Properties", items=get_user_props)
    bpy.types.Scene.operator_property_bone_name = bpy.props.StringProperty()


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    # TODO del properties
    del bpy.types.Scene.target_armature
