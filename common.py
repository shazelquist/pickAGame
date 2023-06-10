#!pickAGame/bin/python
"""
"""
import re
from db import *

scripts = {}
# native_types
# database_types
# make_database_types


def query_input_more(
    query_message="\tDo you want to add more?(Y/n) ", reg=r"^([y](es)?)||([n]o?)$"
):
    accepted = False
    result = ""
    while not accepted:
        result = input(query_message).lower().strip()
        accepted = re.fullmatch(reg, result)
    return result


def type_assertion_regex(typeconf):
    """
    Create a regular expression match function for each type given
    """
    type_regex = {}
    force = lambda x: bool(x)
    # Note: Lambdas only store values as default parameters
    type_regex = lambda x, lab: force(re.fullmatch(typeconf[lab], x))
    return type_regex


def __prepare_scripts__(regex_conf):
    """
    Load config information in each script
    """
    regex = type_assertion_regex(regex_conf)
    # CHECK REGEX
    # for r in regex_conf:
    #    print(r,regex_conf[r])
    #    read=input().strip()
    #    print(f"'{read}'",regex(read,r))
    # TODO May not need to activate all the scripts.
    for mod in scripts:
        # print(scripts, connections)
        scripts[mod].set_db_conn(
            connections[mod], native_types, database_types, make_database_types, regex
        )
        # scripts[mod].main()


def create_missing_scripts(path, names, statuses):
    for name, exists in zip(names, statuses):
        if not exists:
            print(name)
            with open("scripts/Template.py", "r") as source:
                template = source.read()
                # print(template.replace("{game_name}", name))
            with open(path + name + ".py", "w") as target_script:
                target_script.write(template.replace("{game_name}", name))


def import_scripts(path, names, regex_conf):
    """
    Loads all scrips in names under path
    """
    global scripts
    from importlib import import_module

    print(f"loading {path}")
    sys.path.insert(1, path)
    modules = {}
    for name in names:
        modules[name] = import_module(name)
    print(modules.keys())
    scripts = modules
    __prepare_scripts__(regex_conf)


def main():
    config = initialize_db()
    print(config)
    script_status = check_files(
        config["script_path"], config["Schemas"]["Games"].keys(), ext=".py"
    )
    create_missing_scripts(
        config["script_path"], config["Schemas"]["Games"].keys(), script_status
    )
    import_scripts(
        config["script_path"],
        config["Schemas"]["Games"].keys(),
        config["Schemas"]["InputRegex"],
    )
    game_name = "Template"
    print(config["Schemas"]["Games"][game_name])
    scripts[game_name].enter_session(
        config["Schemas"]["Games"][game_name]["Tables"]["Session"], {"SessionID": 1}
    )
    close_connections()


if __name__ == "__main__":
    query_input_more()
    main()
