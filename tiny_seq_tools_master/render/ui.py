# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2023, The SPA Studios. All rights reserved.

import bpy

class TINYRENDER_PT_batch_render(bpy.types.Panel):
    bl_label = "Batch Render"
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "SPA.Sequencer"

    def draw(self, context: bpy.types.Context):
        self.layout.use_property_split = True
        options = context.scene.batch_render_options
        self.layout.prop(options, "media_type")
        self.layout.prop(options, "renderer")
        self.layout.prop(options, "render_engine")
        self.layout.prop(options, "resolution")
        if options.media_type == "MOVIE":
            self.layout.prop(options, "frames_handles")

        self.layout.prop(options, "filepath_pattern")
        self.layout.prop(options, "selection_only")
        box = self.layout.box()
        box.prop(options, "output_scene")
        if options.output_scene:
            col = box.column(align=True)
            col.prop(options, "output_auto_offset_channels")
            col.prop(options, "output_copy_sound_strips")
            col.prop(options, "render_output_scene")
            if options.render_output_scene:
                col.prop(options, "output_render_filepath_pattern")
        self.layout.operator("sequencer.batch_render")


classes = (TINYRENDER_PT_batch_render,)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)