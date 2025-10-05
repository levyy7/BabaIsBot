#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# === DETECT OS AND SET GAME DIRECTORY ===
case "$(uname -s)" in
    Linux*)
        GAME_DIR="$HOME/.steam/debian-installation/steamapps/common/Baba Is You"
        ;;
    Darwin*)
        GAME_DIR="$HOME/Library/Application Support/BabaIsYou"
        ;;
    MINGW*|MSYS*|CYGWIN*)
        GAME_DIR="C:/Program Files (x86)/Steam/steamapps/common/Baba Is You"
        ;;
    *)
        echo "Unknown OS. Please set GAME_DIR manually."
        GAME_DIR=""
        ;;
esac

echo "Detected OS, suggested GAME_DIR=$GAME_DIR"

# === DEFINE PATHS ===
LUA_DIR="$GAME_DIR/Data/Lua"
COMMANDS_DIR="$GAME_DIR/Data/Commands"
IO_FILE_SOURCE="$SCRIPT_DIR/src/api/hooks/io.lua"
IO_FILE_TARGET="$LUA_DIR/io.lua"

# === CREATE FOLDERS IF GAME_DIR IS SET ===
if [ -n "$GAME_DIR" ]; then
    # Lua folder
    mkdir -p "$LUA_DIR"
    # Commands folder
    mkdir -p "$COMMANDS_DIR"

    # Copy io.lua
    if [ -f "$IO_FILE_SOURCE" ]; then
        cp "$IO_FILE_SOURCE" "$IO_FILE_TARGET"
        echo "Copied io.lua to $IO_FILE_TARGET"
    else
        echo "Warning: io.lua not found in current directory, skipping copy"
    fi

    echo "Commands folder ready at $COMMANDS_DIR"
fi

# === SETUP ENV FILE ===
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ".env file created from template"
fi

# Function to set or replace a key in .env
set_env_var() {
    local key=$1
    local value=$2
    if grep -q "^$key=" .env; then
        sed -i.bak "s|^$key=.*|$key=$value|" .env && rm .env.bak
    else
        echo "$key=$value" >> .env
    fi
}

# Write env keys (empty if GAME_DIR not detected)
set_env_var "BABA_SOURCE_DIR" "$GAME_DIR"
set_env_var "BABA_COMMANDS_DIR" "$COMMANDS_DIR"
set_env_var "BABA_LOCALHOST_PORT" "5000"

echo ".env updated with Baba Is You paths (edit manually if needed)"
