def extract_type(archived_text, pair_type):
    return ''.join(str(pair[0]) * pair[1] for pair in archived_text
                   if type(pair[0]) is pair_type)


def reversed_dict(dictionary):
    return {value: key for key, value in dictionary.items()}


def flatten_dict(dictionary, prefix=''):
    flattened = {}
    for key, value in dictionary.items():
        if isinstance(value, dict):
            flattened_value = flatten_dict(value, prefix + key + '.')
            flattened.update(flattened_value)
        else:
            flattened[prefix + key] = value
    return flattened


def unflatten_dict(dictionary):
    unflattened = {}
    for key in dictionary.keys():
        if '.' in key:
            subkeys = key.split('.')
            parent_dict = unflattened.setdefault(subkeys[0], {})
            for subkey in subkeys[1:]:
                if subkey == subkeys[-1]:
                    parent_dict[subkey] = dictionary[key]
                else:
                    parent_dict = parent_dict.setdefault(subkey, {})
        else:
            unflattened[key] = dictionary[key]
    return unflattened


def reps(items):
    return tuple(item for item in items if items.count(item) > 1)