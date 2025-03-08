# py-ollama
# to anyone coders who is looking to this code, pls help me clean these mess. ;-;
# version 0.3dev (not finished) (March-8-'25)
from urllib import response
from httpx import stream
import ollama, rich, os
client = ollama.Client()


def exitprog():
    rich.print("[italic]Exiting...")
    os.system("ollama stop "+modelin)
    if os.name == 'nt':
        os.system("taskkill /im ollama.exe")
    else:
        os.system("killall ollama")
    exit()

def clearout():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")

def pull(usr):
    rich.print(f'[italic]Pulling {usr}...')
    os.system('ollama pull ' + usr)   

def rm(usr):
    rich.print(f'[italic]Removing {usr}...')
    os.system('ollama rm ' + usr)      

def usrcmd(usr):
    # TODO for maintainability: use lambdas instead of going yanderedev mode.
        cmd = usr.split(" ")
        print(cmd)
        commands = {
        "/help": lambda: print('''
/help : Display list of available commands
/exit : Stop running LLMs then exit program.
/list : List all pulled models. (using 'ollama list' command)
/clear: Clear all previous outputs, including those outside py-ollama.
/pull: Pull an available LLM for using locally from ollama.com
/rm : Delete a pulled LLM from your drive.
        '''),
        "/exit": lambda: exitprog(),
        "/list": lambda: os.system('ollama list'),
        "/clear": lambda: clearout(),
        "/pull": lambda: pull(cmd[1]),
        "/rm" : lambda: rm(cmd[1])
    }
        try:
            if usr:
                commands[cmd[0]]()
            else:
                rich.print("[bold red][!] Unknown command.")
        except Exception as e:
            rich.print("[bold red][!] An error has occurred!")



def genchat(usr, modelin):
    try:
        # uhhh what the hell is this mess...
        # TODO for v0.3: Format bold texts with double asterisks and italic texts with backticks.
        if ":" in modelin:
            modelname = list(modelin.split(":"))
        else:
            modelname = list(modelin)
        rich.print(f"[bold]{modelname[0]}:[/bold]")
        rich.print("[grey italic]Thinking...", end="")
        stream = ollama.chat(model=modelin, messages=[{'role': 'user', 'content': usr}], stream=True, )   
        print('\r', end="")
        for chunk in stream:
            rich.print(chunk['message']['content'], end='', flush=True)
        rich.print("\n[italic]Response generated.")
    except Exception as ex:
        rich.print("[bold red][!] An error has occurred")
        print(ex)
        exitprog()
    finally:
        pass

# start here

rich.print("[bold blue]py-[bold yellow]ollama")
rich.print("[bold yellow][i]This is dev build, beware of bugs and errors!")
print("""[Version: 0.3dev - March 08 '25]
      
A Python3-based terminal interface for Ollama.
Please enter model name below to start:""")
while True:
    modelin = str(input("> "))
    if modelin == '/exit':
        rich.print("[italic]Exiting...")
        if os.name == 'nt':
            os.system("taskkill /im ollama.exe")
        else:
            os.system("killall ollama")
        exit()
    elif len(modelin) > 0:
        if modelin[0] == '/':
            usrcmd(modelin)
        else:
            rich.print("\nSelected model:", f"[bold white]{modelin}")
            rich.print("[blue itlaic]Type /help for list of commands.")
            while True:
                usr = str(input(">> "))
                if usr[0] == '/':
                    usrcmd(usr)
                else:
                    genchat(usr, modelin)
    else:
        rich.print("[bold red][!] No model given, exiting...")
        exit()
