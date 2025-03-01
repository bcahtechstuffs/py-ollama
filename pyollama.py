from urllib import response
import ollama, rich, os
client = ollama.Client()
# hi
def genchat(usr, modelin):
    rich.print("[italic]Generating reponse...")
    response = ollama.generate(model=modelin, prompt=usr)
    if ":" in modelin:
        modelname = list(modelin.split(":"))
    else:
        modelname = list(modelin)
    rich.print(f"[bold]{modelname[0]}:", response.response)
    rich.print('''
[italic]Reponse generated.''')

modellst = ollama.list()
# start point
rich.print("[bold blue]py-[bold yellow]ollama")
print("""[Version: 0.1]
      
A Python3-based terminal interface for Ollama.
Please enter model name below to start:""")
modelin = str(input("> "))
if modelin == '/exit':
    print("Exiting...")
    exit()
elif modelin:
    rich.print("Selected model:", f"{modelin}")
    rich.print("[blue]Type /exit to exit program.")
    print("Type your prompt to begin.")
    while True:
        usr = str(input(">> "))
        if usr == "/exit":
            print("Exiting...")
            exit()
        else:
            genchat(usr, modelin)
else:
    rich.print("[bold red][!] No model given, exiting...")
    exit()
