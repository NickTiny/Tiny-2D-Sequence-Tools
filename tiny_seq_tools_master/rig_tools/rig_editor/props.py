import bpy

classes = ()

def bone_items(self, context):
    arma = context.scene.target_armature
    return [(bone.name, bone.name, "") for bone in arma.data.bones]

def bone_groups(self, context):
    bone_groups = context.scene.target_armature.pose.bone_groups
    items =  [(bone_group.name, bone_group.name, "") for bone_group in bone_groups]
    items.append(("All_Bones", "All Bones", ""))
    return items

def find_bones(self,context):
    return context.scene.target_armature.pose.bones
def check_armature(self, object):
    return object.type == "ARMATURE"
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.target_armature = bpy.props.PointerProperty(name="Target Arm", type=bpy.types.Object, poll=check_armature)
    bpy.types.WindowManager.offset_editor_active = bpy.props.BoolProperty(
        name="Offset Editor is Active", default=False
    )
    bpy.types.WindowManager.gpencil_editor_active = bpy.props.PointerProperty(
        type=bpy.types.GreasePencil
    )
    bpy.types.Scene.target_bone = bpy.props.EnumProperty(name="Bones", items=bone_items)
    bpy.types.Scene.target_bone_group = bpy.props.EnumProperty(name="Bone Group",items=bone_groups)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    #TODO del properties 
    del bpy.types.Scene.target_armature
