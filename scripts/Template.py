#!/pickAGame/bin/python
"""
The script for {game_name}
"""

from common import query_input_more

db_conn = False
native_types = {}
database_types = {}
make_database_types = {}
type_regex = {}


def session_input_loop(label, ntype):
    """
    Request user input for a field in the scheme
    And then verify using the regular expression mapped to that scheme

    Returns a field value as a native python type
    """
    incomplete = True
    while incomplete:
        try:
            field = input(f"\tPlease enter a value for {label}")
            incomplete = not type_regex(field, ntype)
            # !UserCustomization!: if you have a custom schemea that links to other {game_name} tables
            #   Insert your check here and replace the value as nessasary!
            #   For repeated input attempts Please set incomplete = True
            if not incomplete:
                print(f"\tError, please enter an {native_type}")
                continue
            trans_field = native_types[ntype](field)
        except Exception as e:
            print(f'Something went wrong: "{e}"')
    return trans_field


def session_input_line(scheme, split=" "):
    """
    Request user input for each field in the scheme
    And then verify using the regular expression mapped to that scheme

    Returns a list of field values as a native python type
    """
    incomplete = True
    labels = split.join(scheme.keys())
    trans_field = {}
    while incomplete:
        # try:
        line = input(
            f"\tPlease enter a value for {labels}, seperated by '{split}'\n\t\t"
        )
        fields = [raw.strip() for raw in line.split(split) if raw]
        # assert(len(fields)==len(scheme.keys()))
        regex_report = [
            type_regex(field, scheme[label])
            for label, field in zip(scheme.keys(), fields)
        ]
        print(regex_report)
        incomplete = (
            not regex_report
            or False in regex_report
            or len(fields) != len(scheme.keys())
        )
        # !UserCustomization!: if you have a custom schemea that links to other {game_name} tables
        #   Insert your check here and replace the value as nessasary!
        #   For repeated input attempts Please set incomplete = True
        if incomplete:
            report = split.join(
                [
                    f"{lab}:{scheme[lab]}"
                    for lab, correct in zip(scheme.keys(), regex_report)
                    if not correct
                ]
            )
            print(f"\tError, These fields had the wrong type {report}")
            continue
        trans_field = {
            col: native_types[scheme[col]](field)
            for col, field in zip(scheme.keys(), fields)
        }
        # except Exception as e:
        #    print(f'Something went wrong: "{e}"')
    return trans_field


def enter_session(session_schema, auto_prop):
    """
    Set session values for {game_name} described in data/schemas.toml
    This method is intended to be updated for extended functionality.

    By default it requests input for each field listed in the schema
    auto_prop contains key value pairs for auto_set or carried values.
    """
    fields = session_schema.copy()
    user_required = {
        field: session_schema[field]
        for field in fields
        if field not in auto_prop.keys()
    }
    rows = []

    more_rows = True
    while more_rows:
        more_rows = False
        new_row = session_input_line(user_required)
        new_row.update(auto_prop)
        rows.append(tuple(new_row.values()))
        more_rows = (
            query_input_more(
                "\tDo you want to add more to this {game_name} session? (y/N) "
            )[0]
            == "y"
        )

    cols = new_row.keys()
    print(rows)
    set_session(session_schema, cols, rows)


def set_session(schema, cols, rows):
    """
    Save the session information for that {game_name}

    Param requirements are built from data/schemas.toml
    Expects:
        set_db to be called before
        schema: key-pair column names to data types to pass to db_types for conversion and storage
        cols:   The names of the columns to insert, in this order
        rows:   The values to insert in the order of cols
    """
    if db_conn:
        curs = db_conn.cursor()
        param_count = ", ".join([f"?" for col in cols])
        columns = ",".join(cols)
        for row in rows:  # Replace with executemany as needed
            print(
                f"INSERT INTO Session({columns}) VALUES({param_count})",
                [
                    make_database_types[schema[col]](field)
                    for col, field in zip(cols, row)
                ],
            )
            curs.execute(
                f"INSERT INTO Session({columns}) VALUES({param_count})",
                [
                    make_database_types[schema[col]](field)
                    for col, field in zip(cols, row)
                ],
            )
    else:
        print("No db connection found")
        # The following is just the same as the above, but it prints instead of executing it
        param_count = ", ".join([f"{col}=?" for col in cols])
        for row in rows:
            print(
                f"INSERT INTO Session VALUES({param_count});",
                [
                    make_database_types[schema[col]](field)
                    for col, field in zip(cols, row)
                ],
            )
            # print(
            #    "\tREGEX Result",
            #    [type_regex(field, schema[col]) for col, field in zip(cols, row)],
            # )


def set_db_conn(db_connection, ntypes, dbtypes, mkdbtypes, reg):
    """
    Keep a connection to the database {game_name}.db
    And maintain the conversion objects required to communicate with it.
    """
    global db_conn, native_types, database_types, make_database_types, type_regex
    db_conn = db_connection
    native_types = ntypes
    database_types = dbtypes
    make_database_types = mkdbtypes
    type_regex = reg


def main():
    print("template")
    enter_session({"SessionID": "int", "map": "str"}, {"SessionID": 1})
    return
    set_session(
        **{
            "cols": ["SessionID"],  # "Mode", "D", "B", "F"],
            "schema": {
                "SessionID": "int",
                # "Mode": "str",
                # "D": "date",
                # "B": "bool",
                # "F": "float",
            },
            "rows": [
                *[(str(i),) for i in range(1, 20)]
                # ("1", "mode1", "1111-11-11", "T", "0"),
                # ("2", "mode2", "2222-22-22", "True", "0.0"),
                # ("3", "mode3", "3333-33-33", "False", "111111111111.11"),
                # ("4", "mode4", "4444-44-44", "FALSE", "0.33333333333"),
            ],
        }
    )


if __name__ == "__main__":
    main()
