# INSTALL INSTRUCTIONS

Just a heads up, this is not that simple of an installation, mostly because I dont really want to deal with filepaths, but just follow along and everyhing should be fine

FOR ARCH LINUX ONLY!!!


#I Setting up the venv

1. create a new python virtual environment with python venv -m venv

2. source into the venv with: source venv/bin/activate

3. Install the contets of the requirements.txt with pip install


#II Getting the rest working

1. Download the latest version of python

2. Download Ollama (sudo pacman -Syu ollama - for CPU) (sudo pacman -Syu ollama-cuda - for NVIDIA GPU) (sudo pacman -Syu ollama-rocm - for AMD GPU)

3. Get the models you want to use, in this case: ollama pull deepseekr1:14b, ollama pull nomic-embed-text", ollama pull qwen3:0.6b

4. Clone the repository, or just download the important files

5. Open request_handler.py - in here fine the COMMUNICATION_FILE_LOCATION variable, and change it to the location of the file.txt file that is located the same folder as the script.

6. Open sky.sh - in here change venv_location, python_script_location and communication_file_location to their appropriate values, look at the existing locations for referance

7. Install the zed text editor (sudo pacman -Syu zed) OR change the display editor in the sky.sh file

8. Optional: Go into answer_web.py and answer.pt - here you can change what models ollama program will use

9. Run the sky.sh script from the terminal (you can also setup a custom keybinding to run the script)
