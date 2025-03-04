# py-ollama
from urllib import response
from httpx import stream
import ollama, rich, os
client = ollama.Client()
# hi
def usrcmd(usr, modelin):
    if usr == '/help':
        print(''' py-ollama commands:
/help : Display list of available commands (which is this)
/exit : Stop running LLMs then exit program.
/list : List all pulled models. (using 'ollama list' command)
''')
    if usr == '/exit':
        rich.print("[italic] Exiting...")
        os.system("ollama stop "+modelin)
        exit()
    if usr == '/list':
        os.system('ollama list')


def genchat(usr, modelin):
    try:
        rich.print("[italic]Generating response...")
        stream = ollama.chat(model=modelin, messages=[{'role': 'user', 'content': usr}], stream=True, )
        if ":" in modelin:
            modelname = list(modelin.split(":"))
        else:
            modelname = list(modelin)
        rich.print(f"[bold]{modelname[0]}:[/bold]")
        # uhhh what the hell is this mess...
        for chunk in stream:
            rich.print(chunk['message']['content'], end='', flush=True)
        print("\n")
        rich.print("[italic] Response generated.")
    except Exception as ex:
        rich.print("[bold red][!] An error has occurred")
        print(ex)
        os.system("ollama stop " + modelin)
        print("Exiting py-ollama")
    finally:
        pass

# start here

rich.print("[bold blue]py-[bold yellow]ollama")
print("""[Version: 0.2]
      
A Python3-based terminal interface for Ollama.
Please enter model name below to start:""")
while True:
    modelin = str(input("> "))
    if modelin == '/exit':
        os.system("killall ollama")
        rich.print("[italic]Exiting...")
        exit()
    elif modelin == '/help':
        usrcmd(modelin, modelin)
    elif modelin == '/list':
        usrcmd(modelin, modelin)


    elif modelin:
        rich.print("Selected model:", f"[bold white]{modelin}")
        rich.print("[blue]Type /help for list of commands.")
        while True:
            usr = str(input(">> "))
            if usr[0] == '/':
                usrcmd(usr, modelin)
            else:
                genchat(usr, modelin)
    else:
        rich.print("[bold red][!] No model given, exiting...")
        exit()
