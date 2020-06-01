import json
import copy
import re as regex

ARGUMENTS_KEY = "__args"
RENAME_KEY = "__name"


# Main function: get a dict and convert it into a gql query
def dict_to_graphql(dict_query: dict) -> str:
    dict_query = copy.deepcopy(dict_query)  # Clone in order not to change origin

    query = _convert_dict_to_gql_query(dict_query)
    query = "query {{ {0} }}".format(query)
    return query


# Convert dict to gql keys
def _convert_dict_to_gql_query(dict_query: dict) -> str:
    query = ""

    for dict_field_name, dict_field in dict_query.items():
        field_to_query = ""

        if dict_field is True:
            field_to_query = dict_field_name
        elif isinstance(dict_field, dict):
            field_to_query = _process_dict_field(dict_field_name, dict_field)

        query += "{0}\r\n".format(field_to_query)

    return query


def _process_dict_field(name: str, dict_query: dict) -> str:
    args = ""
    rename = ""

    if ARGUMENTS_KEY in dict_query:
        args = dict_to_args(dict_query.pop(ARGUMENTS_KEY))
    if RENAME_KEY in dict_query:
        rename = dict_query.pop(RENAME_KEY)
    if rename is not "":
        name = "{}:{}".format(rename, name)     # Convert name

    sub_query = _convert_dict_to_gql_query(dict_query)
    query = """
    {0}{1} {{
        {2}
    }}
    """
    query = query.format(name, args, sub_query)

    return query


def dict_to_args(args: dict) -> str:
    if len(args) == 0:
        return ""

    args = [
        "{}: {}".format(arg_key, _process_arg(arg_val))
        for arg_key, arg_val in args.items()
    ]
    args = "({})".format(", ".join(args))   # Convert the array to (k1:v1, k2: v2, ...)

    return args


def _process_arg(arg):
    if isinstance(arg, map):
        arg = list(arg)    # If it's a map object, return it into a list
    if isinstance(arg, str):
        arg = f'"{arg}"'
    if isinstance(arg, int):
        arg = str(arg)
    if isinstance(arg, list):
        arg = [_process_arg(x) for x in arg]     # Preprocess all values on args in list
        arg = ", ".join(arg)
        arg = "[{}]".format(arg)
    if isinstance(arg, dict):
        arg = remove_json_key_quotes(json.dumps(arg))

    return arg


def remove_json_key_quotes(value) -> str:
    return regex.sub(r'"(.*?)"(?=:)', r'\1', value)
