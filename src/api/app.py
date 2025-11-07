from flask import Flask, request, jsonify
import os
import configparser
import time
import json

from src.api.server_utils import read_world_state, get_next_command_file

app = Flask(__name__)

COMMAND_LIST = {"LEFT", "RIGHT", "UP", "DOWN", "STILL"}


# --- API ENDPOINTS ---

@app.route("/game_state", methods=["GET"])
def get_game_state():
    """
    Returns a formatted, plain-text grid representing the current level layout.
    """
    try:
        units, room_size = read_world_state()

        # Convert position and layer from string to integer for calculations
        for u in units:
            u["XPOS"] = int(u["XPOS"])
            u["YPOS"] = int(u["YPOS"])
            u["ZLAYER"] = int(u["ZLAYER"])

        if room_size and room_size[0] > 2 and room_size[1] > 2:
            min_x, min_y = 1, 1
            max_x, max_y = room_size[0] - 2, room_size[1] - 2
        else:
            if not units:
                return jsonify({"error": "No units found and no room size available."}), 404
            min_x = min(u["XPOS"] for u in units)
            max_x = max(u["XPOS"] for u in units)
            min_y = min(u["YPOS"] for u in units)
            max_y = max(u["YPOS"] for u in units)

        pos_map = {}
        for u in units:
            key = (u["XPOS"], u["YPOS"])
            if key not in pos_map:
                pos_map[key] = []
            pos_map[key].append((u["ZLAYER"], u["UNITNAME"]))
        for v in pos_map.values():
            v.sort()

        first_col_width = max(len("y/x"), max((len(str(y)) for y in range(min_y, max_y + 1)), default=0), 3)
        col_widths = {}
        for x in range(min_x, max_x + 1):
            maxlen = max((len(",".join(name for _, name in pos_map.get((x, y), []))) for y in range(min_y, max_y + 1)),
                         default=0)
            col_widths[x] = max(maxlen, 5)

        lines = []
        header = ["y/x".ljust(first_col_width)] + [f"{x}".center(col_widths.get(x, 5)) for x in range(min_x, max_x + 1)]
        lines.append(" | ".join(header))
        lines.append(
            "-" * first_col_width + "-+-" + "-+-".join(["-" * col_widths.get(x, 5) for x in range(min_x, max_x + 1)]))

        for y in range(min_y, max_y + 1):
            row = [f"{y}".ljust(first_col_width)]
            for x in range(min_x, max_x + 1):
                cell = pos_map.get((x, y), [])
                cell_content = ",".join([name for z, name in cell])
                row.append(cell_content.ljust(col_widths.get(x, 5)))
            lines.append(" | ".join(row))

        return "<pre>" + "\n".join(lines) + "</pre>"

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/execute_commands", methods=["POST"])
def execute_commands():
    """
    Creates a command file to execute a list of gameplay commands.
    """
    data = request.get_json(force=True)
    commands: list[str] = data.get("commands", "")
    try:
        for cmd in commands:
            if cmd.upper() not in COMMAND_LIST:
                return jsonify({"error": f"Invalid command: {cmd}. Valid commands are: {', '.join(COMMAND_LIST)}"}), 400
        if not commands:
            return jsonify({"error": "No valid commands provided"}), 400

        command_file = get_next_command_file()
        # Assumes a global `command(name, type)` function exists in your Lua script.
        with open(command_file, "w", encoding="utf-8") as f:
            f.write("\n".join([f'command("{cmd.lower()}",1)' for cmd in commands]) + "\n")

        return jsonify({
            "status": "success",
            "message": f"Command file created with commands: {', '.join(commands)}",
            "file_created": command_file
        })
    except Exception as e:
        return jsonify({"error": f"Error executing commands: {str(e)}"}), 500


@app.route("/undo_multiple", methods=["POST"])
def undo_multiple():
    """
    Creates a command file to execute 'n' undo commands.
    """
    data = request.get_json(force=True)
    n = data.get("n")
    if not isinstance(n, int) or n <= 0:
        return jsonify({"error": "Parameter 'n' must be a positive integer"}), 400
    try:
        command_file = get_next_command_file()
        # Assumes a global `undo()` function exists in your Lua script.
        with open(command_file, "w", encoding="utf-8") as f:
            f.write("\n".join(["undo()" for _ in range(n)]) + "\n")
        return jsonify({
            "status": "success",
            "message": f"Command file created for {n} undo operations.",
            "file_created": command_file
        })
    except Exception as e:
        return jsonify({"error": f"Error undoing moves: {str(e)}"}), 500


@app.route("/restart_level", methods=["POST"])
def restart_level():
    """
    Restarts the current level by simulating an 'r' keypress.
    """
    try:
        command_file = get_next_command_file()

        # This uses the RestartLevel function from your main.lua script.
        command_content = 'RestartLevel()'
        with open(command_file, "w", encoding="utf-8") as f:
            f.write(command_content)

        return jsonify({
            "status": "success",
            "message": "Command file created to restart level",
            "file_created": command_file
        }), 201
    except Exception as e:
        return jsonify({"error": f"Error restarting level: {str(e)}"}), 500


@app.route('/load_level', methods=['POST'])
def load_level():
    """
    Creates a command file to load a specific level file.
    """
    data = request.get_json()
    if not data or 'level_id' not in data:
        return jsonify({"status": "error", "message": "Missing 'level_id' in request body"}), 400

    level_id = data['level_id']
    if not type(level_id) == int:
        return jsonify({"status": "error", "message": "Invalid level_id format."}), 400

    level_name = f"{level_id}level"
    command_file = get_next_command_file()

    # This uses the GoToLevel function from your main.lua script.
    command_content = f'GoToLevel("{level_name}")'
    try:
        with open(command_file, "w", encoding="utf-8") as f:
            f.write(command_content)

        return jsonify({
            "status": "success",
            "message": f"Command file created to load level: {level_name}",
            "file_created": command_file
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": f"An internal error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)