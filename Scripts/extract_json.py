#!/usr/bin/env python3
import inspect
import json
import re
import sys
from typing import List, Dict

help_menu = inspect.cleandoc(
    """
    extract_json.py <json> <path> [--require-simple] [-v|--verbose]

    Inspired by lodash.get

    <json> is a json object (as a string)

    <path> is a deep-path string ('a.1.b.2'). For each '.' delimted
    value, if the current nested element is an object, will get the value
    of the property. if the current nested element is a list AND the current
    lookup value is a number, will return the 0-indexed item in the list.
    If <path> is not valid, will exit with code 1.
    You can escape literal '.' characters with '\.'

    [--require-simple] By default if <path> points to a complex object (a
    list or another object) in <json> the string representation of that
    object will be returned. If --require-simple is passed in, and <path>
    points to a complex object, will exit with code 2.

    [-v|--verbose] Print error messages.
    """
)


def parse_path(path_str: str) -> List[str]:
    """Use negative look behind assertion regex for magix spliting while respecing escaped '.'s"""
    return re.split(r"(?<!\\)\.", path_str)


def parse_args(args: List[str]) -> (Dict, List[str], bool, bool):
    if len(args) < 2:
        raise ValueError("Bad number of arguments")
    require_simple = "--require-simple" in args[2:]
    verbose = "-v" in args[2:] or "--verbose" in args[2:]
    try:
        json_dict = json.loads(args[0])
    except:
        raise ValueError("Invalid json for first object")
    json_path = parse_path(args[1])
    return json_dict, json_path, require_simple, verbose

def traverse_json(json_dict: Dict, json_path: List[str]):
    cur_obj = json_dict
    for item in json_path:
        if type(cur_obj) == dict:
            if str(item) in cur_obj:
                cur_obj = cur_obj[str(item)]
            else:
                raise ValueError("Object is missing specified item")
        elif type(cur_obj) == list:
            try:
                item = int(item)
            except:
                raise ValueError("Can not look up item from list with non-integer item")
            if item < len(cur_obj):
                cur_obj = cur_obj[item]
            else:
                raise ValueError("List too small to look up given index")
    return cur_obj


args = sys.argv[1:]

help_menu_requested = len(args) == 1 and ("-h" in args or "--help" in args)
if help_menu_requested or len(args) == 0:
    print(help_menu)
    sys.exit(0)

try:
    json_dict, json_path, require_simple, verbose = parse_args(args)
except ValueError as err:
    print(err)
    sys.exit(-1)

try:
    item_at_path = traverse_json(json_dict, json_path)
except ValueError as err:
    if verbose:
        print(err)
    sys.exit(1)

item_at_path_is_complex = type(item_at_path) in [dict, list]
if require_simple and item_at_path_is_complex:
    if verbose:
        print("Encounterd non-simple value")
    sys.exit(2)

print(str(item_at_path))
