def remove_keys_from_dict(keys_list, dict):
    for key in keys_list:
        if key in dict: del dict[key]
