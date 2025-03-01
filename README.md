# py-ollama
*"basically Ollama but with extra steps"*

A Python-based terminal interface for Ollama.
> [!NOTE]  
> This program is in its **EARLY STAGE**, which mean bugs can occur and missing a lot of features.
> Also, its dev is lazy.
 
## Requirements
- Ollama installed
- Python 3.8 or later
- Internet connection (for downloading required files, models)
<details>
<summary>Quick start guide</summary>

  # Quick start guide
  
  ### 1. Preparing
  Assuming you have Python 3.8 (or later) and Ollama are already installed.
  Check if your Python install is compatible by running `py` or `python3` in terminal.
  If Python is installed, terminal should output like this:
  ```
  > py
  Python 3.12.7 (main, Feb  4 2025, 14:46:03) [GCC 14.2.0] on linux
  Type "help", "copyright", "credits" or "license" for more information.
  >>> 
  ```
  Otherwise, go to https://www.python.org/downloads/ to download Python.
  
  ### 2. Running py-ollama
  Download or clone the repo.
  Install required dependencies from text file `requirements.txt`:
  ```
  py -m pip install -r requirements.txt
  ```
  Download your desired model for Ollama by running:
  ```
  ollama pull [model]
  ```
  with [model] is a name of your chosen model.
  All downloadable models can be found here https://ollama.com/search
  
  Example:
  ```
  ollama pull llama3.2:1b
  ```
  The command above is used to pull a version of `llama3.2` model with 1 billion parameters for low-end computers.
  
  Run `py-ollama.py` with:
  ```
  py pyollama.py
  ```
  Follow the program instructions.
</details>
