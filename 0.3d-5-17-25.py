# py-ollama: alternative front-end for ollama
# noob "software engineer" with his ever-so-finest creation
# version 0.3dev (May-17-'25)


import rich
rich.print("[italic]Starting py-ollama...")
w = 0
t = 0
messages = []
print('\r', end="")
try:
    from urllib import response
    from httpx import stream
    import ollama, os, re, time, subprocess
except ModuleNotFoundError as e:
    rich.print("[bold red](x) Missing dependencies")
    rich.print("[white] Your python install is missing modules which are [white bold]required[/white bold] for py-ollama.")
    rich.print("[white] You can install them by running ""python3 -m pip install -r requirements.txt"" within py-ollama folder.")
    exit()
client = ollama.Client()
modelin = ""


def stat(modelin, t, w):
    rich.print("[bold]Stat for previous output")
    print(f"Model:       {modelin}")
    if t < 1000:
        print(f"Time:        {t} ms")
    else:
        t2 = round(round(t) / 1000)
        print(f"Time:        {t} ms (~{t2} s)")
    print(f"Word count:  {w}")


def format_rich_text(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'[bold]\1[/bold]', text)
    text = re.sub(r'\*(.*?)\*', r'[italic]\1[/italic]', text)
    text = re.sub(r'_(.*?)_', r'[italic]\1[/italic]', text)
    text = re.sub(r'`(.*?)`', r'[white on black]\1[/white on black]', text)
    return text

def exitprog():
    rich.print("[italic]Exiting...")
    if modelin:
        subprocess.run(["ollama", "stop", modelin], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.name == 'nt':
        subprocess.run(['taskkill', '/f', '/im', 'ollama'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.run(["killall", "ollama"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    exit()

def clearout():
    global messages
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")
    messages = []

def pull(usr):
    rich.print(f'[italic]Pulling [white italic]{usr}...[/white italic]')
    os.system('ollama pull ' + usr)   

def rm(usr):
    rich.print(f'[italic]Removing [white italic]{usr}...[/white italic]')
    os.system('ollama rm ' + usr)      

def modelswap(usr):
    global modelin
    modelin = usr
    rich.print(f"[white italic]Loading {usr}...")
    try: 
        ollama.chat(model=modelin, messages=[{'role': 'user', 'content': "hi"}])
    except Exception as e:
        rich.print("[bold red](!) An error has occurred")
        rich.print(f"[red]{e} ({e.__traceback__})")
        exitprog()
    return str(modelin)

def mlist():
    os.system('ollama list')
    rich.print("\nTo view a list of models available for pull, visit https://ollama.com/search")


def usrcmd(usr):
        cmd = usr.split(" ")
        commands = {
        "/help": lambda: print('''py-ollama commands (commands followed by underscore requires a additional argument):
/help : Display list of available commands
/exit : Stop running LLMs then exit program.
/list : List all pulled models. ('ollama list')
/clear: Clear all previous outputs.
/pull _: Pull an available LLM for using locally ('ollama pull')
/rm _ : Delete a pulled LLM from your drive. ('ollama rm')
/change _ : Switch to another model.
/stat: Show statistics for previous response.
        '''),
        "/exit": lambda: exitprog(),
        "/list": lambda: mlist(),
        "/clear": lambda: clearout(),
        "/pull": lambda: pull(cmd[1]) if len(cmd) > 1 else rich.print("[bold red](!) Missing model name"),
        "/rm" : lambda: rm(cmd[1]) if len(cmd) > 1 else rich.print("[bold red](!) Missing model name"),
        "/change" : lambda: modelswap(cmd[1]) if len(cmd) > 1 else rich.print("[bold red](!) Missing model name"),
        "/stat" : lambda: stat(modelin, t, w)
    }
        try:
            if usr and cmd[0] in commands:
                commands[cmd[0]]()
            elif usr:
                rich.print("[bold red](!) Unknown command.")
        # except Exception as e:
        #     rich.print("[bold red](!) An error has occurred!")
        #     rich.print(f"[bold red]{e}")
        #     exitprog()
        finally:
            pass



def genchat(usr, modelin):
    try:
        global w, t
        isReasoning = False
        # uhhh what the hell is this mess...
        if ":" in modelin:
            modelname = list(modelin.split(":"))
        else:
            modelname = list(modelin)
        rich.print(f"[bold]{modelname[0]}:[/bold]")
        rich.print("[grey italic]Thinking...", end="")
        # Legacy fallback output
        # stream = ollama.chat(model=modelin, messages=[{'role': 'user', 'content': usr}], stream=True)   
        # print('\r', end="")
        # for chunk in stream:
        #     formatted_text = format_rich_text(chunk['message']['content'])
        #     rich.print(formatted_text, end='', flush=True)
        # rich.print("\n[italic]Response generated.")

        # Newer output code with context
        messages.append({'role': 'user', 'content': usr})
        w=0
        t=0
        start = time.time()
        stream = ollama.chat(model=modelin, messages=messages, stream=True) 

        print('\r', end="")
        assistant_response = ""
        for chunk in stream:
            content = chunk['message']['content']
            assistant_response += content 
            formatted_text = format_rich_text(content) 
            rich.print(formatted_text, end='', flush=True)
            w += 1
        end = time.time()
        t = (end-start)*10**3
        rich.print("\n[italic]Response generated.")
        messages.append({'role': 'assistant', 'content': assistant_response})

    # except Exception as e:
    #     rich.print("[bold red](!) An error has occurred")
    #     rich.print(f"[red]{e}")
    #     exitprog()
    finally:
        pass


# start here
rich.print("[bold blue]py-[bold yellow]ollama")
rich.print("[bold yellow](i) This is dev build, beware of imcomplete features and stuffs!")
print("""[Version: 0.3dev - May 17 '25]
      
A Python3-based and terminal-based front-end interface for Ollama.
Please enter model name below to start:""")

def starter():
    global modelin
    while True:
        modelin = str(input("> "))
        if len(modelin) == 0:
            rich.print("[bold red] (x) No input found")
            continue
        if modelin == '/exit':
            exitprog()
        if len(modelin) > 0:
            if modelin[0] == '/':
                usrcmd(modelin)
                continue
            else:
                rich.print("\nSelected model:", f"[bold white]{modelin}")
                rich.print("\n[italic]Loading model...")
                try:
                    ollama.chat(model=modelin, messages=[{'role': 'user', 'content': "hi"}])
                except ollama.ResponseError as e:
                    rich.print("[bold red](x) Model doesn't exist")
                    rich.print(f"[red]{e} ({e.__traceback__})")
                    continue
                except Exception as e:
                    rich.print("[bold red](x) An error has occurred")
                    rich.print(f"[red]{e} ({e.__traceback__})")
                    exitprog()
                finally:
                    pass
                rich.print("[green]Model loaded!")  
                rich.print("[blue italic]Type [white]/help[/white] for list of commands.")
                return modelin
modelin = starter()
while True:
    usr = str(input(">> "))
    if usr[0] == '/':
        usrcmd(usr)
    else:
        genchat(usr, modelin)