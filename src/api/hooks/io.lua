function string:split(delimiter)
    local result = {}
    for match in (self .. delimiter):gmatch("(.-)" .. delimiter) do
        table.insert(result, match)
    end
    return result
end

-- At the start of each level, write the current world state to the file.
table.insert(mod_hook_functions["level_start"], function()
    local gates = MF_findgates()
    for key, gateid in pairs(gates) do
        local gate = mmf.newObject(gateid)
        for k,v in pairs(gate) do
            print(k, v)
        end
    end
    local units = MF_getunits()
    local state_data = {}

    for key, unitid in pairs(units) do
        local unit = mmf.newObject(unitid)
        if unit.strings[UNITNAME] ~= "undefined" and unit.flags[DEAD] == false then
            local unit_data = {
                key,
                unit.strings[UNITNAME],
                unit.strings[UNITTYPE],
                unit.values[XPOS],
                unit.values[YPOS],
                unit.values[DIR],
                unit.strings[VISUALDIR],
                unit.values[ZLAYER],
                unit.strings[MOVED],
                unit.values[EFFECT],
                unit.strings[COLOUR],
                unit.strings[VISUALSTYLE],
                unit.strings[VISUALLEVEL],
                unit.strings[CLEARCOLOUR],
                unit.strings[DECOR],
                unit.strings[ONLINE],
                unit.strings[COMPLETED],
                unit.strings[EFFECTCOUNT],
                unit.strings[FLOAT],
                unit.strings[A],
                unit.strings[ID],
            }
            table.insert(state_data, table.concat(unit_data, "|"))
        end
    end

    local state_string = table.concat(state_data, "€")
    MF_store("world", "state", "state", state_string)

    -- Store room size information
    MF_store("world", "state", "room_size", roomsizex .. "|" .. roomsizey)

    -- Initialize the last processed command file number
    MF_store("world", "file", "last_processed", "0")

    print("World state saved.")
end)

-- Global list to hold the sequence of movement commands to execute.
local movement_commands = {}
-- Global variable to track the key of the last command set that was executed.
local last_command_key = 0
local command_check_time = 0
local command_check_interval = 1000 -- Check every 60 frames (approximately 1 second at 60 FPS)

-- Function to check for a new command file and update world state if found
local function check_and_execute_command_file()
    local command_file = "Data/Commands/" .. tostring(last_command_key) .. ".lua"
    local success, err = pcall(function() dofile(command_file) end)
    if success then
        last_command_key = last_command_key + 1
        -- After executing a command file, update the world state as in level_start
        local units = MF_getunits() or {}
        local state_data = {}
        for key, unitid in pairs(units) do
            local unit = mmf.newObject(unitid)
            if unit.strings[UNITNAME] ~= "undefined" and unit.flags[DEAD] == false then
                local unit_data = {
                    key,
                    unit.strings[UNITNAME],
                    unit.strings[UNITTYPE],
                    unit.values[XPOS],
                    unit.values[YPOS],
                    unit.values[DIR],
                    unit.strings[VISUALDIR],
                    unit.values[ZLAYER],
                    unit.strings[MOVED],
                    unit.values[EFFECT],
                    unit.strings[COLOUR],
                    unit.strings[VISUALSTYLE],
                    unit.strings[VISUALLEVEL],
                    unit.strings[CLEARCOLOUR],
                    unit.strings[DECOR],
                    unit.strings[ONLINE],
                    unit.strings[COMPLETED],
                    unit.strings[EFFECTCOUNT],
                    unit.strings[FLOAT],
                    unit.strings[A],
                    unit.strings[ID]
                }
                table.insert(state_data, table.concat(unit_data, "|"))
            end
        end
        local state_string = table.concat(state_data, "€")
        MF_store("world", "state", "state", state_string)

        -- Store room size information
        MF_store("world", "state", "room_size", roomsizex .. "|" .. roomsizey)

        -- Store the last processed command file number
        MF_store("world", "file", "last_processed", tostring(last_command_key - 1))

        print("World state saved after command.")
    end
end

-- This function runs on every game frame.
table.insert(mod_hook_functions["always"], function(extra)
    local current_time = extra[1]
    if current_time - command_check_time > command_check_interval then
        command_check_time = current_time
        check_and_execute_command_file()
    end

end)

table.insert(mod_hook_functions["level_win"], function()
    print("!!! LEVEL WON !!!")
    if MF_read("level","general","name") ~= "map" then
        MF_store("world", "status", "level_won", "true")
    end
end)