#!pickAGame/bin/python
"""
Main app

Two main flows
1 Enter information to store a session
2 Retrieve information to make a decision on which option to play
"""
from sys import argv
from common import *


def session_flow(config):
    """
    Standard input session

        1 Resolve game name
        2 Create new session
        3 Input session information
    """
    # Start input
    game_name = ""
    names = []
    if len(argv) > 1:
        game_name = argv[1]
    while not names:
        if not game_name:
            game_name = input("Enter A game name ").strip()
        # print(f'Searching for {game_name}')
        names = resolve_aliases(
            game_name,
            config["Schemas"]["pAG"]["Sessions"]["Aliases"]["ResolveAliases"],
        )
        game_name = ""
        print(f"\tGame options {names}")
        if len(names) != 1:
            names = []
    game_name = names[0]

    # Import scripts for that game
    scripts = import_scripts(
        config["script_path"],
        [game_name],
        config["Schemas"]["InputRegex"],
    )
    print("scripts:", scripts)
    # Create a session
    s_id = create_new_session(game_name, config["Schemas"]["pAG"]["Sessions"]["Create"])
    # input extra data per that game's session schema
    scripts[game_name].enter_session(
        config["Schemas"]["Games"][game_name]["Tables"]["Session"], {"SessionID": 1}
    )
    # commit

    close_connections()


def options_flow(config):
    """
    Show options weighted by events and last session
    """

    pass


def main():
    # Preinitizalization work if nessasary
    config = initialize_db()
    check_examples_against_regex(
        config["Schemas"]["InputRegexExamples"],
        type_assertion_regex(config["Schemas"]["InputRegex"]),
    )
    script_status = check_files(
        config["script_path"], config["Schemas"]["Games"].keys(), ext=".py"
    )
    create_missing_scripts(
        config["script_path"], config["Schemas"]["Games"].keys(), script_status
    )

    session_flow(config)


if __name__ == "__main__":
    main()
