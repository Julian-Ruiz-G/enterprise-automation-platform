def get_changes(old, new):
    changes = {}

    old_data = old.model_dump() if hasattr(old, "model_dump") else old.__dict__
    new_data = new.model_dump() if hasattr(new, "model_dump") else new.__dict__

    for key in new_data:

        if old_data.get(key) != new_data.get(key):

            changes[key] = {
                "old": old_data.get(key),
                "new": new_data.get(key)
            }

    return changes