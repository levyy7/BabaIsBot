--[[
    BABA IS YOU - MOD HOOK SCRIPT
    This script adds a command system to interface with an external API.
--]]

-- Utility function to split strings.
function string:split(delimiter)
    local result = {}
    for match in (self .. delimiter):gmatch("(.-)" .. delimiter) do
        table.insert(result, match)
    end
    return result
end

-- Global function to be called from command files for level switching.
function GoToLevel(level_name)
    if type(level_name) ~= "string" or level_name == "" then
        print("ERROR: GoToLevel command received an invalid or empty level name.")
        return
    end

    if generaldata == nil then
        print("ERROR: The global 'generaldata' object is not available. Cannot switch levels.")
        return
    end

    -- Construct the full path. The user only needs to provide the level's filename.
    local full_level_path = "Data/Worlds/baba/" .. level_name .. ".l"

    print("COMMAND RECEIVED: Attempting to enter level -> " .. level_name)
    print("Constructed level file path: " .. full_level_path)

    -- Before trying anything, make sure the level file actually exists.
    if not MF_findfile(full_level_path) then
        print("ERROR: Level file not found at path: " .. full_level_path)
        return
    end

    -- STEP 1: Set the game's high-level state variable.
    generaldata.strings[CURRLEVEL] = level_name
    print("Game state updated: CURRLEVEL is now '" .. level_name .. "'")

    -- STEP 2: Manually load the new map data into memory.
    MF_loadtilemap(full_level_path)
    print("Loaded tilemap data from " .. full_level_path)

    -- STEP 3: Force a full restart. The game will now use the pre-loaded map data.
    MF_restart(true)
    print("Forced a level restart to correctly load and display the new level.")
end

function RestartLevel()
    MF_restart(true)
end

-- Global variables for command processing
local last_command_key = 0
local command_check_time = 0
local command_check_interval = 1000 -- Check every 1000ms (1 second)
local is_command_key_initialized = false

-- This function scans the command directory to find the next command to execute.
-- This makes the system resilient to game restarts.
local function initialize_command_key()
    if is_command_key_initialized then return end

    print("Initializing command key from file system...")

    local i = 0
    while true do
        local command_file = "Data/Commands/" .. tostring(i) .. ".lua"
        if not MF_findfile(command_file) then
            -- We've found the first file that doesn't exist.
            -- This means the next command to execute is i.
            break
        end
        i = i + 1
    end

    -- The next command to look for is 'i'.
    last_command_key = i
    -- The last command that was processed is 'i - 1'.
    local max_num = i - 1

    if max_num > -1 then
        print("Highest command file found: " .. max_num .. ".lua")
    else
        print("No existing command files found. Starting command key at 0.")
    end

    is_command_key_initialized = true
    print("Command key initialized. Will start checking for file: " .. last_command_key .. ".lua")
    -- Store the number of the last known command file.
    MF_store("world", "file", "last_processed", tostring(max_num))
end


-- At the start of each level, write the current world state to the file.
table.insert(mod_hook_functions["level_start"], function()
    -- This ensures the command key is synchronized only once per level load.
    print("Current level id: " .. generaldata.strings[CURRLEVEL])
    initialize_command_key()

    local units = MF_getunits()
    local state_data = {}
    for key, unitid in pairs(units) do
        local unit = mmf.newObject(unitid)
        if unit.strings[UNITNAME] ~= "undefined" and unit.flags[DEAD] == false then
            local unit_data = {
                key, unit.strings[UNITNAME], unit.strings[UNITTYPE], unit.values[XPOS],
                unit.values[YPOS], unit.values[DIR], unit.strings[VISUALDIR],
                unit.values[ZLAYER], unit.strings[MOVED], unit.values[EFFECT],
                unit.strings[COLOUR], unit.strings[VISUALSTYLE], unit.strings[VISUALLEVEL],
                unit.strings[CLEARCOLOUR], unit.strings[DECOR], unit.strings[ONLINE],
                unit.strings[COMPLETED], unit.strings[EFFECTCOUNT], unit.strings[FLOAT],
                unit.strings[A], unit.strings[ID],
            }
            table.insert(state_data, table.concat(unit_data, "|"))
        end
    end

    local state_string = table.concat(state_data, "€")
    MF_store("world", "state", "state", state_string)
    MF_store("world", "state", "room_size", roomsizex .. "|" .. roomsizey)
    print("World state saved.")
end)


-- Function to check for a new command file and execute it
local function check_and_execute_command_file()
    local command_file = "Data/Commands/" .. tostring(last_command_key) .. ".lua"

    if MF_findfile(command_file) then
        print("Found command file: " .. command_file)
        -- pcall safely executes the file, preventing crashes from malformed commands.
        local success, err = pcall(function() dofile(command_file) end)

        if success then
            print("Successfully executed command file.")
            -- Update the last processed command file number in storage.
            MF_store("world", "file", "last_processed", tostring(last_command_key))
            -- Increment key to look for the next file.
            last_command_key = last_command_key + 1
        else
            print("ERROR executing command file: " .. tostring(err))
            -- Increment the key anyway to avoid getting stuck on a bad file.
            last_command_key = last_command_key + 1
        end

        -- After executing, immediately save the world state.
        local units = MF_getunits() or {}
        local state_data = {}
        for key, unitid in pairs(units) do
            local unit = mmf.newObject(unitid)
            if unit.strings[UNITNAME] ~= "undefined" and unit.flags[DEAD] == false then
                local unit_data = {
                    key, unit.strings[UNITNAME], unit.strings[UNITTYPE], unit.values[XPOS],
                    unit.values[YPOS], unit.values[DIR], unit.strings[VISUALDIR],
                    unit.values[ZLAYER], unit.strings[MOVED], unit.values[EFFECT],
                    unit.strings[COLOUR], unit.strings[VISUALSTYLE], unit.strings[VISUALLEVEL],
                    unit.strings[CLEARCOLOUR], unit.strings[DECOR], unit.strings[ONLINE],
                    unit.strings[COMPLETED], unit.strings[EFFECTCOUNT], unit.strings[FLOAT],
                    unit.strings[A], unit.strings[ID]
                }
                table.insert(state_data, table.concat(unit_data, "|"))
            end
        end
        local state_string = table.concat(state_data, "€")
        MF_store("world", "state", "state", state_string)
        MF_store("world", "state", "room_size", roomsizex .. "|" .. roomsizey)
        print("World state saved after command execution.")
    end
end

-- This function runs on every game frame.
table.insert(mod_hook_functions["always"], function(extra)
    -- Ensure initialization has run before checking for commands.
    if not is_command_key_initialized then return end

    local current_time = extra[1]
    if current_time - command_check_time > command_check_interval then
        command_check_time = current_time
        check_and_execute_command_file()
    end
end)

table.insert(mod_hook_functions["level_win"], function()
    print("!!! LEVEL WON !!!")
    if MF_read("level", "general", "name") ~= "map" then
        MF_store("world", "status", "level_won", "true")
    end
end)

