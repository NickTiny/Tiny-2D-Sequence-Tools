import string
import bpy


def sync_selection_to_viewport(strip):
    scene = strip.id_data
    if scene.selection_to_active:
        scene.sequence_editor.active_strip = strip
        return True
    return False


def sync_seq_camera_to_viewport(strip):
    updated_viewport = False
    scene = strip.id_data
    if not scene.link_seq_to_3d_view:
        updated_viewport = False
        return updated_viewport
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            bpy.context.scene.camera = bpy.data.objects[
                strip.scene_camera.name
            ]  # Select camera as view
            area.spaces.active.region_3d.view_perspective = "CAMERA"  # Use camera view
            updated_viewport = True
    return updated_viewport


def make_render_scene(context):
    scene_name = "RENDER"
    user_scene_name = str(context.scene.name)
    for scene in bpy.data.scenes:
        if scene.name == scene_name:
            bpy.ops.scene.delete({"scene": bpy.data.scenes[scene_name]})

    bpy.ops.scene.new("INVOKE_DEFAULT", type="EMPTY")
    bpy.context.scene.sequence_editor_create()
    bpy.context.scene.name = scene_name
    render_scene = bpy.data.scenes[scene_name]
    context.window.scene = bpy.data.scenes[f"{user_scene_name}"]

    # Copy Strips
    context.scene.frame_set(1)
    bpy.ops.sequencer.select_all(action="SELECT")
    bpy.ops.sequencer.copy()

    # Paste Strips
    context.window.scene = render_scene
    context.scene.frame_set(1)
    bpy.ops.sequencer.paste()
    context.window.scene = bpy.data.scenes[f"{user_scene_name}"]
    return render_scene, user_scene_name
