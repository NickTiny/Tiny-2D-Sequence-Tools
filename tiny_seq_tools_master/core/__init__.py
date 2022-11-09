from tiny_seq_tools_master.core import save_pre, sync_core, load_post


def register():
    sync_core.register()
    save_pre.register()
    load_post.register()


def unregister():
    sync_core.unregister()
    save_pre.unregister()
    load_post.unregister()
