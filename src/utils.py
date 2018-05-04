# coding: utf-8
"""
This module contains various utils function at global usage.
"""

import logging


def init_logger(pattern, pattern_debug, level):
    """
    Init the logger, loading configuration from config file.
    Args:
        pattern (unicode): Pattern for the logger.
        pattern_debug (unicode): Pattern for the logger in debug mode.
        level (lvl): Level of the logger.
    """
    pattern = pattern_debug if level == logging.DEBUG else pattern
    formatter = logging.Formatter(pattern)
    logger = logging.getLogger()

    if not logger.handlers:
        handler = logging.StreamHandler()
    else:
        handler = logger.handlers[0]

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)

def json_set(item, path, value):
    """
    Set the value corresponding to the path in a dict.
    Arguments:
        item (dict): The object where we want to put a field.
        path (unicode): The path separated with dots to the field.
        value: The value to set on the field.
    Return:
        (dict): The updated object.
    """
    tab = path.split(u".")
    if tab[0] not in item and len(tab) > 1:
        item[tab[0]] = {}
    if len(tab) == 1:
        item[tab[0]] = value
    else:
        item[tab[0]] = json_set(item[tab[0]], u".".join(tab[1:]), value)
    return item


def json_del(item, path):
    """
    Delete the item corresponding to path of the field in a dict.
    Arguments:
        item (dict): The object where we want to delete a field.
        path (unicode): The path separated with dots to the field.
    Return:
        The value.
    """
    tab = path.split(u".")
    if tab[0] in item:
        if len(tab) > 1:
            return json_del(item[tab[0]], u".".join(tab[1:]))
        else:
            del item[tab[0]]

    return item


def json_get(item, path, default=None):
    """
    Return the path of the field in a dict.
    Arguments:
        item (dict): The object where we want to put a field.
        path (unicode): The path separated with dots to the field.
        default: default value if path not found.
    Return:
        The value.
    """
    tab = path.split(u".")

    if isinstance(item, dict) and tab[0] in item:
        if len(tab) > 1:
            return json_get(item[tab[0]], u".".join(tab[1:]), default=default)
        return item[tab[0]]

    return default


def json_to_one_level(obj, parent=None):
    """
    Take a dict and update all the path to be on one level.
    Arguments:
        output (dict): The dict to proceed.
        parent (unicode): The parent key. Used only with recursion.
    Return:
        dict: The updated obj.
    """

    output = {}
    for key, value in obj.items():
        if isinstance(value, dict):
            if parent is None:
                output.update(json_to_one_level(value, key))
            else:
                output.update(json_to_one_level(value, u".".join([parent, key])))
        elif isinstance(value, list):
            for index, item in enumerate(value):
                item = {
                    unicode(index): item
                }
                if parent is None:
                    output.update(json_to_one_level(item, u".".join([key])))
                else:
                    output.update(json_to_one_level(item, u".".join([parent, key])))
        else:
            if parent is not None:
                output[u".".join([parent, key])] = value
            else:
                output[key] = value
    return output


def sublist_split(items, parts=None, count_per_sublist=None):
    """
    This method split a list of items in several sub lists to make paralleling process easier.

    Args:
        items (list): A list of items to split in parts..
        parts (int): Number of part.
        count_per_sublist (int): Number of item per list.

    Returns:
        (list): A list of lists.
    """
    # XOR
    if not ((parts and not count_per_sublist) or (not parts and count_per_sublist)):
        raise ValueError(u"You need to specify parts or count_per_sublist parameters")

    output = []

    # Mod 1
    if parts:
        count_per_sublist = int(math.ceil(len(items) / parts))

    # Mod 2
    if count_per_sublist:
        parts = int(math.ceil(len(items) / count_per_sublist))
        for index in range(0, parts + 1):
            sub_part = items[index * count_per_sublist:index * count_per_sublist + count_per_sublist]
            if sub_part:
                output.append(sub_part)
    return output


def get_json_differences(item_a, item_b):
    """
    Return differences between two JSON.

    Args:
        item_a (dict): object to compare.
        item_b (dict): object to compare.

    Returns:
        (tuple): differences, (removed, udpated, added)
    """
    item_a = json_to_one_level(item_a)
    item_b = json_to_one_level(item_b)
    obj_a_items = json_to_one_level(item_a).items()
    obj_b_items = json_to_one_level(item_b).items()
    obj_a_keys = [item[0] for item in obj_a_items]
    obj_b_keys = [item[0] for item in obj_b_items]
    updated = [(key, value) for key, value in obj_b_items if key in obj_a_keys and value != item_a[key]]
    removed = [(key, value) for key, value in obj_a_items if key not in obj_b_keys]
    added = [(key, value) for key, value in obj_b_items if key not in obj_a_keys]
    return removed, updated, added


def check_and_get_data(data, rules, strict=False):
    """
    This methods check a payload to see if some rules are valid (Does have a specific parameter, is it required, ...)
    Args:
        data (dict): The data to check.
        rules (list): A list of tuples (path_to_field(unicode), type, is_required(bool)).
        strict (boolean): If strict is false, the function try to cast. Else it throws an error.

    Returns:
        (tuple): A tuple of three lists : (data, missing, wrong)
    """
    missing = []
    wrong = []

    def check_rule(field, required_types, is_required, default_val=None):
        """
        Sub method to check rules.
        Args:
            field (unicode): The field path.
            required_types (list): The types we want to get.
            is_required (boolean): Is it required or not.
            default_val: An eventual default value if the thing is not there.
        """
        # Transform in list if necessary.
        required_types = required_types if isinstance(required_types, list) else [required_types]

        # Get the value
        value = json_get(data, field)
        if not strict and isinstance(value, list) and list not in required_types and len(value) == 1:
            value = value[0]

        # test if value exist, knowing it is required.
        if value is None and is_required:
            if default_val is None:
                missing.append(field)
            else:
                value = default_val

        # Test if type is right in the given list.
        type_found = None
        for typ in required_types:
            if not callable(typ) and isinstance(value, typ):
                type_found = typ

        # Try a cast.
        if value is not None and not type_found and not strict:
            for typ in required_types:
                try:
                    if typ is dict and isinstance(value, (unicode, str)):
                        value = json.loads(value)

                    elif callable(typ):
                        value = typ(value)
                    else:
                        value = typ(value)
                    type_found = typ
                except Exception:
                    pass

        if not type_found and value is not None:
            wrong.append(field)

        if value is not None:
            json_set(data, field, value)

    # For each rule
    for rule in rules:
        check_rule(*(rule))

    return data, missing, wrong


def check_string_list_param(value):
    """
    This method parse a string into a list.
    Args:
        value (uniode): The list to parse.

    Returns:
        (list): The parsed list.
    """
    tab = value.split(u",")
    if not tab:
        return False

    return [unicode(item) for item in tab]

def check_int_list_param(value):
    """
    This method parse a string into a list.
    Args:
        value (uniode): The list to parse.

    Returns:
        (list): The parsed list.
    """
    tab = value.split(u",")
    if not tab:
        return False

    return [int(item) for item in tab]


def check_unicode_list_param(value):
    """
    This method parse a string into a list.
    Args:
        value (uniode): The list to parse.

    Returns:
        (list): The parsed list.
    """
    tab = value.split(u",")
    if not tab:
        return False

    return [unicode(item) for item in tab]
