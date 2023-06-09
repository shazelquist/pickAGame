# Goals
 - should be very easy to update information as this will happen a lot.
 - should be easy to pull out information and give a degree of choice to match other lax restrictions.
 - should be able to retrieve and store metadata
 - should be able to add games/modes relatively easily
 - Mixers are variable, and should be organized by each game
 - Should be somewhat testable

## Direction:
 May consider using a config file to adjust the hierarchy and inclusion of mixers
 Data may be a sort of dynamically structured database: yaml -> table

 yaml -> table is too much for the scope of this project, let's just build things modularly and get it done.

 Database per Game, also just a session database that holds information like the date

 Build a timeline based on dates

 How are we going to test this, Most of it should be data integ


## Data:

 - Game
 * Mixers
    - modes
    - maps
    - mixers
    - characters
    - roles
    - issues
    - deadlines
    - mission
    - Difficulty
  - Session
    - Date
    - What was done

### Example Structure

Games
    l4d2
        Decisional:
            Maps, Mode (This can be seen pairwise, most of the time mode->maps)
                No Mercy, Crash Course, Death Toll, Dead Air, Blood Harvest, The Sacrifice
        Informational:
            Characters
            Campaign length/Difficulty/Errors/Description
            
    DeepRockGalactic
        Decisional:
            Event, Deadline
            Weekly Corehunt/priority/deepdive
    
    RiskOfRain
        Decisional:
            Characters
                Commando, Mercenary, Rex
            Ending
                Mithrix, Scavenger, Voidling
        
    RiskOfRain



### New Structure

Session
    Date
    Game
    Session ID

Events
    Game
    Deadline
    Description

DeepRockGalactic
    Session ID

RiskOfRain
    Session ID

    Ending

    Endings

Left4Dead
    Session ID

    Map
    Mode


    Maps



