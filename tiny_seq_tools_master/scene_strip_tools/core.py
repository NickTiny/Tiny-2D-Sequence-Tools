import bpy


def make_render_scene(context: bpy.types.Context) -> (bpy.types.Scene):
    """Create Scene called 'RENDER' from current scene settings, and copy all strips into it."""
    scene_name = "RENDER"
    user_scene = context.scene

    for scene in bpy.data.scenes:
        if scene.name == scene_name:
            bpy.ops.scene.delete({"scene": bpy.data.scenes[scene_name]})

    render_scene = context.scene.copy()
    render_scene.name = scene_name

    for strip in render_scene.sequence_editor.sequences_all:
        if strip.type == "SCENE":
            strip.scene = user_scene

    for col in render_scene.collection.children:
        render_scene.collection.children.unlink(col)
    for obj in render_scene.collection.objects:
        render_scene.collection.objects.unlink(obj)

    for collection in render_scene.collection.children:
        scene.collection.children.unlink(collection)

    render_scene.render.use_sequencer = True

    context.window.scene = user_scene
    return render_scene


def get_scene_strip_cameras(scene):
    return sorted(
        (
            obj
            for obj in scene
            if obj.type == "CAMERA" and obj.name != scene.line_art_cam_name
        ),
        key=lambda x: x.name,
    )
