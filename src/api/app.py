from flask import Flask, request, jsonify
import os
import configparser
import time
import json

from src.api.server_utils import read_world_state

app = Flask(__name__)


@app.route("/game_state", methods=["GET"])
def get_game_state():
    try:
        units, room_size = read_world_state()

        for u in units:
            u["XPOS"] = int(u["XPOS"])
            u["YPOS"] = int(u["YPOS"])
            u["ZLAYER"] = int(u["ZLAYER"])

        if room_size is not None:
            min_x, min_y = 1, 1
            max_x, max_y = room_size[0] - 2, room_size[1] - 2
        else:
            if not units:
                return (
                    jsonify({"error": "No units found and no room size available."}),
                    404,
                )
            min_x = min(u["XPOS"] for u in units) + 1
            max_x = max(u["XPOS"] for u in units) - 1
            min_y = min(u["YPOS"] for u in units) + 1
            max_y = max(u["YPOS"] for u in units) - 1

        pos_map = {}
        for u in units:
            key = (u["XPOS"], u["YPOS"])
            if key not in pos_map:
                pos_map[key] = []
            pos_map[key].append((u["ZLAYER"], u["UNITNAME"]))
        for v in pos_map.values():
            v.sort()

        first_col_width = max(
            len("y/x"), max(len(str(y)) for y in range(min_y, max_y + 1)), 3
        )
        col_widths = {}
        for x in range(min_x, max_x + 1):
            maxlen = 0
            for y in range(min_y, max_y + 1):
                cell = pos_map.get((x, y), [])
                if len(cell) > 1:
                    cell_content = ",".join([name for z, name in cell])
                    print(cell_content)
                elif len(cell) == 1:
                    cell_content = cell[0][1]
                else:
                    cell_content = ""
                maxlen = max(maxlen, len(cell_content))
            col_widths[x] = max(maxlen, 5)

        lines = []
        header = ["y/x".ljust(first_col_width)] + [
            f"{x}".center(col_widths[x]) for x in range(min_x, max_x + 1)
        ]
        lines.append(" | ".join(header))
        lines.append(
            "-" * first_col_width
            + "-+-"
            + "-+-".join(["-" * col_widths[x] for x in range(min_x, max_x + 1)])
        )

        for y in range(min_y, max_y + 1):
            row = [f"{y}".ljust(first_col_width)]
            for x in range(min_x, max_x + 1):
                cell = pos_map.get((x, y), [])
                if len(cell) > 1:
                    cell_content = ",".join([name for z, name in cell])
                elif len(cell) == 1:
                    cell_content = cell[0][1]
                else:
                    cell_content = ""
                row.append(cell_content.ljust(col_widths[x]))
            lines.append(" | ".join(row))

        return "<pre>" + "\n".join(lines) + "</pre>"

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/execute_commands", methods=["POST"])
def execute_commands():
    data = request.get_json(force=True)
    commands = data.get("commands", "")
    try:
        command_list = [cmd.strip() for cmd in commands.split(",")]
        for cmd in command_list:
            if cmd not in COMMAND_LIST:
                return (
                    jsonify(
                        {
                            "error": f"Invalid command: {cmd}. Valid commands are: {', '.join(COMMAND_LIST)}"
                        }
                    ),
                    400,
                )
        if not command_list:
            return jsonify({"error": "No valid commands provided"}), 400

        command_file = get_next_command_file()
        with open(command_file, "w", encoding="utf-8") as f:
            f.write("\n".join([f'command("{cmd}",1)' for cmd in command_list]) + "\n")

        config = configparser.ConfigParser()
        config.read(STATE_PATH, encoding="utf-8")
        level_won_status = config.get("status", "level_won", fallback="unknown")

        if level_won_status == "true":
            return jsonify(
                {
                    "result": "Level won! You can now enter another level to earn more points."
                }
            )
        else:
            return jsonify(
                {
                    "result": "Commands executed successfully. You have not yet won the level, please continue."
                }
            )

    except Exception as e:
        return jsonify({"error": f"Error executing commands: {str(e)}"}), 500


@app.route("/undo_multiple", methods=["POST"])
def undo_multiple():
    data = request.get_json(force=True)
    n = data.get("n")
    if not isinstance(n, int) or n <= 0:
        return jsonify({"error": "Parameter 'n' must be a positive integer"}), 400
    try:
        command_file = get_next_command_file()
        with open(command_file, "w", encoding="utf-8") as f:
            f.write("\n".join(["undo()" for _ in range(n)]) + "\n")
        result = execute_control_file_and_wait(command_file)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": f"Error undoing moves: {str(e)}"}), 500


@app.route("/restart_level", methods=["POST"])
def restart_level():
    try:
        click_to_focus_game()
        pyautogui.press("r")
        return jsonify({"result": "Restarted the current level"})
    except Exception as e:
        return jsonify({"error": f"Error restarting level: {str(e)}"}), 500
