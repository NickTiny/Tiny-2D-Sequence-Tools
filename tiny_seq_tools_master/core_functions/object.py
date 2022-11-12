import bpy


def check_object_type(obj: bpy.types.Object, type: str) -> bool:
    if obj.type == type:
        return True


def get_consts_on_obj(obj: bpy.types.Object, type: str) -> list:
    return [constraint for constraint in obj.constraints if constraint.type == type]
