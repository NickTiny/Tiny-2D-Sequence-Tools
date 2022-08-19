import bpy


class SEQUENCER_PT_line_art(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_line_art_tools"
    bl_label = "Line"
    bl_category = "Strip"

    def all_status_true(context):
        for item in context.scene.line_art_load.load:
            if item.status == False:
                return False
        return True

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        box = col.box()
        box.prop(
            context.scene.line_art_load,
            "load",
            slider=False,
            expand=False,
            icon="FILE_REFRESH",
        )
        if context.scene.line_art_load.error == False:
            box.prop(
                context.scene.line_art_load,
                "error",
                slider=False,
                expand=False,
                icon="ERROR",
                text="A Strip has Error",
            )

        for item in context.active_sequence_strip.line_art_list:
            row = box.row()
            row.prop(
                item, "thickness", slider=False, expand=False, text=item.object.name
            )

            if item.status == False:
                row.alert = True
                row.prop(
                    item,
                    "status",
                    slider=False,
                    expand=False,
                    icon="ERROR",
                    icon_only=True,
                )
                row.operator("view3d.key_line_art", icon="LOOP_BACK", text="RESET")


classes = (SEQUENCER_PT_line_art,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
