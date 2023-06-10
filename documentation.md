# pickAGame

## Format
```
    main
        db.py
            db.toml
                data/schemas.toml
        sessions.py
            scripts/{games}.py
                data/{games}.db
        events.py
```
### sessions.py

#### Points of interest
 - IsDue: Check each game and calculate the order of preference (date.now()-lastplayed)/(std(daysdiff)), Return N best results.
 - schemas.toml/db.py: FirstTimeSetup enables you to set manually generate tables for that database instead of automatically generating it from the present tables defintion
 - !UserCustomization! is a tag that you can search for to customize and edit portions of this application
 - Move aliases to a central database instead of querying multiple
 - Need to fully initialize pAG databases before working on Games so that aliases can be properly updated with a basic case for each game's name
 - Make an actual init script and possibly a wizzard for generating new Games (might require toml writer)


### scripts/{game}.py
 - This is copied from scripts/Template.py so that custom methods and behaviors can be written for each game.

#### Required methods (subject to change, these files are too busy)
 - set_db: Save the database connection
 - set_session: Data saved after session
 - get_options: Get reccomendations for that game


## Stretch
 - Can probably port this over and integrate the interface into some sort of bot for discord since that's where this would probably be used.
 - Automatic table linking from schema.
 - Refactor for other subjects like meals & recipies.
 - Calender-type integrations and recurring events.
