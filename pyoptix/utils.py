import os
import fnmatch


def find_sub_path(sub_path, search_paths):
    import os.path

    for search_path in search_paths:
        path = os.path.join(search_path, sub_path)
        if os.path.exists(path):
            return path

    raise ValueError('Sub-path not found in searched paths: {0}'.format(sub_path))


def is_2_string_tuple(obj):
    return isinstance(obj, tuple) and len(obj) == 2 \
           and isinstance(obj[0], str) and isinstance(obj[1], str)


def is_4_string_tuple(obj):
    return isinstance(obj, tuple) and len(obj) == 4 \
           and isinstance(obj[0], str) and isinstance(obj[1], str) \
           and isinstance(obj[2], str) and isinstance(obj[4], str)


def glob_recursive(path, pattern):
    matches = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(dirpath, filename))
    return matches
