#!/usr/bin/env bash
set -euo pipefail

venv_location="/home/zippy/Scripts/Sky/venv/bin/activate"
python_script_location="/home/zippy/Scripts/Sky/request_handler.py"
communication_file_location="/home/zippy/Scripts/Sky/file.txt"

prompt=$(zenity --entry --title="
Sky.ai" --text="Type !w at the beggining to use web searching" --entry-text "")


if [[ $prompt = "" ]]; then
     exit 1
fi 

source $venv_location

python $python_script_location $prompt

#zeditor is a simple text editor I use to open and preview the file, feel free to change it to whatever you want
zeditor $communication_file_location 

