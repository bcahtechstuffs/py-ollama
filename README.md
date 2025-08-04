# py-ollama
*"basically Ollama but with extra steps"*

A Python-based terminal interface for Ollama.
> [!IMPORTANT]  
> You are in **dev** branch of py-ollama, which means all of releases which is for this branch, has unfinished and/or buggy codes.
> Ok but, 0.4 might have gigatons of more feature (still, Textual will be used for 0.5)

 ## Requirements
- **Ollama** installed  
- **Python 3.8 or later**  
- **Internet connection** (for downloading required files and models)  

---

<details>
<summary>Quick Start Guide</summary>

### 1 **Verifying Python install**  
Ensure you have **Python 3.8 or later** and **Ollama** installed.  
To verify your Python installation, run the following in your terminal:  
```
py --version   # For Windows
python3 --version  # For macOS/Linux
```
If Python is installed, you should see output like this:  
```bash
Python 3.12.7 (main, Feb 4 2025, 14:46:03) [GCC 14.2.0] on linux
```
If not, download Python from [python.org](https://www.python.org/downloads/).  

---

### 2 **Setting Up py-ollama**  
1. **Clone the Repository**  
   ```
   git clone -b dev https://github.com/bcahtechstuffs/py-ollama
   cd py-ollama
   ```

2. **Install Dependencies**  
   ```
   py -m pip install -r requirements.txt
   ```

3. **Downloading model**  
   Use Ollama to pull a model:  
   ```
   ollama pull <model-name>
   ```
   Replace `<model-name>` with your desired model. You can browse available models at [Ollama Search](https://ollama.com/search).

   **Example:**  
   ```bash
   ollama pull llama3.2:1b
   ```
   This pulls the `llama3.2` model with 1 billion parameters, optimized for low-end computers.  

---

### 3 **Running the Application**  
Execute the script:  
```
# For Windows:
py pyollama.py

# For macOS/Linux:
python3 pyollama.py
```
Follow the on-screen instructions.  

</details>
