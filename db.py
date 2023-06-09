#!pickAGame/bin/python
"""
Provide means to access Each database
Running as main should check that each database exists and create it if it does not
"""

import tomli
import sqlite3 as sql
from os.path import isfile
from datetime import date
import sys

# convert input and database values into native types
native_types = {
    "int": int,
    "float": float,
    "date": date.fromisoformat,
    "str": str,
    "bool": lambda x: x == "T" or x.lower == "true",
}
# intermediate type lable to database types
database_types = {
    "int": "INTEGER",
    "float": "REAL",
    "date": "TEXT",
    "str": "TEXT",
    "bool": "TEXT",
}
passthrough = lambda x: x
# convert native types into database types
make_database_types = {
    "int": passthrough,
    "float": passthrough,
    "str": passthrough,
    "date": lambda x: x.isoformat(),
    "bool": lambda x: "T" * int(x) + "F" * (not x),
}
# database connections
connections = {}


def get_db_config(path="db.toml"):
    """
    Open and parse the database configuration file(s)
    """
    with open(path) as conf:
        config = tomli.loads(conf.read())
    if "game_schemas" in config:
        with open(config["game_schemas"]) as games:
            config["Schemas"]["Games"] = tomli.loads(games.read())
            config["databases"] += config["Schemas"]["Games"].keys()
    return config


def check_files(path, items, ext=".db"):
    """
    Given a path, and some items, check if they exist
    """
    exists = []
    for fname in items:
        filepath = path + fname + ext
        if not isfile(filepath):
            print(f"\tFile not found {filepath}")
            exists.append(False)
        else:
            exists.append(True)
    return exists


def open_connections(path, dbs, ext=".db"):
    for db in dbs:
        connections[db] = sql.connect(path + db + ext)
        print(f"\t {db}{ext} Opened")


def close_connections():
    for dbname in connections:
        connections[dbname].commit()
        connections[dbname].close()
        print(f"\t {dbname}.db Closed")


def create_db(name, config):
    newdb = sql.connect(name)
    # do something to insert based on the config
    curs = newdb.cursor()
    print(f"\n\nDatabase {name}\n{config}")
    init = "FirstTimeSetup"
    if init in config:
        ins = config[init]
        print("predef", ins)
        curs.execute(config[init])
    else:
        for table in config["Tables"]:
            explicit = [
                "{} {}".format(col, database_types[config["Tables"][table][col]])
                for col in config["Tables"][table]
            ]
            cols = ", ".join(explicit)
            # cols = ", ".join(config["Tables"][table]) # Non Explicit types
            ins = f"CREATE TABLE IF NOT EXISTS {table}({cols});"
            curs.execute(ins)
    newdb.close()


def create_missing_dbs(path, names, statuses, schemas, ext=".db"):
    for name, exists in zip(names, statuses):
        print(name, exists)
        if not exists:
            create_db(path + name + ext, schemas[name])


def create_missing_scripts(path, names, statuses):
    for name, exists in zip(names, statuses):
        if not exists:
            print(name)
            with open("scripts/Template.py", "r") as source:
                template = source.read()
                # print(template.replace("{game_name}", name))
            # with open(path+name+'.py','w') as target_script:
            # target_script.write(template.replace('{game_name}', name))


def initialize_db():
    # load the config file
    config = get_db_config()
    # config["databases"] = [
    #    "Template"
    # ]  # Temporary overwrite for testing "Sessions","Events",

    for conf_type in ["pAG", "Games"]:
        db_status = check_files(config["db_path"], config["Schemas"][conf_type].keys())
        create_missing_dbs(
            config["db_path"],
            config["Schemas"][conf_type].keys(),
            db_status,
            config["Schemas"][conf_type],
        )

    open_connections(config["db_path"], config["Schemas"]["Games"].keys())
    return config


def main():
    initialize_db()
    close_connections()


if __name__ == "__main__":
    main()
