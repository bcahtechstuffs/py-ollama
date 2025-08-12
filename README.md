# py-ollama
*"basically Ollama but with extra steps"*

![le graphics](https://github.com/bcahtechstuffs/py-ollama/blob/main/decorator/pyollamashowcase.gif)

A Python-based terminal interface for Ollama to run LLMs locally (with slightly better output).
> [!IMPORTANT]  
> This program is in its **EARLY STAGE** and **INCOMPLETE**, which mean bugs can occur and missing a lot of features.
>

 
## Requirements
- Ollama installed
- Python 3.8 or later
- Internet connection (for downloading required files, models)
<details>
<summary>Guide</summary>

  # Quick start guide
  
  ### 1. Preparing
  Assuming you have Python 3.8 (or later) and Ollama are already installed.
  Check if your Python install is compatible by running `py` or `python3` in terminal.
  If Python is installed, terminal should output like this:
  ```
  Python 3.12.7 (main, Feb  4 2025, 14:46:03) [GCC 14.2.0] on linux
  Type "help", "copyright", "credits" or "license" for more information.
  >>> 
  ```
  Otherwise, go to https://www.python.org/downloads/ to download Python interpreter.
  
  Also ensure Ollama is installed on your computer. If not, visit https://ollama.com/download and follow instruction to install Ollama
  
  ### 2. Running py-ollama
  Download or clone this repository. You can clone this repository with Git by running this command:
  ```
  git clone https://github.com/bcahtechstuffs/py-ollama
  ```
  You can also download the program in `Releases` page of this repository.
  
  Install required dependencies from text file `requirements.txt`:
  ```
  py -m pip install -r requirements.txt
  ```
  Run `py-ollama` by running:
  ```
  # Windows
  py pyollama.py
  # Linux/macOS
  python3 pyollama.py
  ```
  then run:
  ```
  >> /pull [model]
  ```
  with `[model]` is name followed by amount of parameters (if have one) of your desired model.
  
  All downloadable models can be found here https://ollama.com/search
  
  Example:
  ```
  >> /pull llama3.2:1b
  ```
  The command above is used to pull a version of `llama3.2` model with 1 billion parameters for low-end computers.

  After pulling model, type your previously pulled model name to begin chatting.
  Follow on-screen instructions.
</details>
