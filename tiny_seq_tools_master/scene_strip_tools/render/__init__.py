# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2023, The SPA Studios. All rights reserved.

from tiny_seq_tools_master.scene_strip_tools.render import (
    props,
    ops,
)

# Borrowed from https://github.com/The-SPA-Studios/sequencer-addon


def register():
    props.register()
    ops.register()

def unregister():
    props.unregister()
    ops.unregister()
