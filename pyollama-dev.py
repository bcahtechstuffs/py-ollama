# py-ollama: alternative front-end for ollama
# version 0.4dev
# last edited = 28th August '26
# TODO : implement file reading, remote network access
# whatever this is

# import modules
try:
    import rich
    from rich.panel import Panel
    from rich.live import Live
    from rich.text import Text
    from rich.markdown import Markdown
    # from textual.app import App, ComposeResult # coming soon i think
    rich.print("[italic]Starting py-ollama...", end="\r")
except ModuleNotFoundError:
    print("(x) Missing dependencies")
    print("Your Python install is missing rich module which is required for displaying formatted output.")
    print("You can install them by running `python3 -m pip install -r requirements.txt` within py-ollama folder.")
    exit()

try:
    import ollama, os, time, subprocess, datetime, sys, getpass
    from urllib.parse import urlparse
except ModuleNotFoundError as e:
    if os.name == "nt":
        rich.print(Panel.fit(f"""[bold red](x) Missing dependencies[/bold red]
[red]{e}[/red]
[white]Your Python install is missing module(s) which are [white bold]required[/white bold] for py-ollama.
You can install them by running `py -m pip install -r requirements.txt` withnin py-ollama folder.""", border_style="red"))
        exit()
    else:
        rich.print(Panel.fit(f"""[bold red](x) Missing dependencies[/bold red]
[red]{e}[/red]
[white]Your Python install is missing module(s) which are [white bold]required[/white bold] for py-ollama.
You can install them by running `python3 -m pip install -r requirements.txt` withnin py-ollama folder.""", border_style="red"))
        exit()
# end of import modules

class pyollama:
    def __init__(self):
        self.client = ollama.Client()
        self.modelin = ""
        self.messages = []
        self.word_count = 0
        self.response_time = 0
        self.console = rich.console.Console()
        self.rawoutput = False
        self.refreshSpeed = 12
        self.fileReady = False
        self.fileLocation = None
        self.fileContent = None
        self.server_url = "http://127.0.0.1:11434"
        self.remote_server = False

    def network_access(self, server_url=None): # connect to a local or LAN Ollama server
        server_url = server_url or input("(n) Ollama server address: ").strip()
        if not server_url:
            rich.print(Panel.fit("[bold red](!) No server address entered.[/bold red]", border_style="red"))
            return False
        if "://" not in server_url:
            server_url = f"http://{server_url}"

        parsed_url = urlparse(server_url)
        if parsed_url.scheme not in ("http", "https") or not parsed_url.hostname:
            rich.print(Panel.fit("[bold red](!) Use an address such as 192.168.1.50:11434.[/bold red]", border_style="red"))
            return False
        if parsed_url.path not in ("", "/") or parsed_url.query or parsed_url.fragment:
            rich.print(Panel.fit("[bold red](!) The server address must not include a path or query.[/bold red]", border_style="red"))
            return False

        normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        try:
            new_client = ollama.Client(host=normalized_url)
            new_client.list()
        except Exception as e:
            rich.print(Panel.fit(f"""[bold red](!) Could not connect to Ollama server.[/bold red]
[white]{e}
[bold yellow] Consider checking if the server is running and accessible.[/bold yellow]""", border_style="red"))
            return False

        self.client = new_client
        self.server_url = normalized_url
        self.remote_server = parsed_url.hostname not in ("127.0.0.1", "localhost", "::1")
        rich.print(f"[green](i) Connected to Ollama at [bold white]{self.server_url}")
        return True
        

    def read_file(self): # file reading (W.I.P)
        # prompt for file path, normalize and validate before reading
        filePath = input("(f) Enter path to file: ").strip()
        if not filePath:
            rich.print(Panel.fit(f"[bold red](!) No path entered.[/bold red]", border_style="bold red"))
            return
        testFilepath = os.path.abspath(os.path.expanduser(filePath))
        try:
            if not os.path.exists(testFilepath) or not os.path.isfile(testFilepath):
                rich.print(Panel.fit(f"[bold red](!) File does not exist.[/bold red]", border_style="bold red"))
                return
            with open(testFilepath, 'r', encoding='utf-8', errors='replace') as fl:
                self.fileContent = fl.read()
            self.fileReady = True
            rich.print(Panel.fit(f"[bold green](i) File loaded: {testFilepath}[/bold green]", border_style="green"))
        except PermissionError:
            rich.print(Panel.fit(f"[bold red](!) Cannot read this file due to missing permission(s).[/bold red]", border_style="bold red"))
        except Exception as e:
            rich.print(Panel.fit(f"""[bold red](!) An error has occurred.[/bold red]
[white]{e}""", border_style="bold red"))
        self.fileLocation = testFilepath



    def exit_prog(self): # exit program
        rich.print("[italic]Exiting...")
        if self.modelin and not self.remote_server:
            try:
                subprocess.run(["ollama", "stop", self.modelin], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            except subprocess.CalledProcessError:
                rich.print(Panel.fit("""[bold yellow](!) It appears that active LLM(s) can't be stopped normally[/bold yellow]
You may need to terminate all Ollama processes manually""", border_style="yellow"))
        if self.remote_server:
            exit()
        if os.name == 'nt':
            subprocess.run(['taskkill', '/f', '/im', 'ollama'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(["killall", "ollama"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        exit()

    def clear_output(self): # clear terminal and conversation history
        if os.name == 'nt':
            os.system("cls")
        else:
            os.system("clear")
        self.messages = []

    def pull_model(self, model_name): # pull a model from ollama.com/search
        rich.print(f'[italic]Pulling [white italic]{model_name}...[/white italic]')
        try:
            for progress in self.client.pull(model=model_name, stream=True):
                status = progress.get("status") if isinstance(progress, dict) else getattr(progress, "status", None)
                if status:
                    rich.print(f"[dim]{status}[/dim]", end="\r")
            rich.print(f"\n[green](i) Model '{model_name}' pulled successfully.")
        except Exception as e:
            rich.print(Panel.fit(f"""[bold red](!) Unable to pull model.[/bold red]
[white]{e}""", border_style="red"))

    def remove_model(self, model_name): # delete a model from disk
        rich.print(f'[italic]Removing [white italic]{model_name}...[/white italic]')
        try:
            self.client.delete(model=model_name)
            rich.print(f"[green](i) Model '{model_name}' removed successfully.")
        except Exception as e:
            rich.print(Panel.fit(f"""[bold red](!) Unable to remove model.[/bold red]
[white]{e}""", border_style="red"))

    def switch_model(self, new_model_name): # stop currently running model and use different one
        rich.print(f"[italic]Loading [white bold]{new_model_name}[/white bold]...")
        try:
            self.client.chat(model=new_model_name, messages=[{'role': 'user', 'content': "hi"}])
            self.modelin = new_model_name
            rich.print(f"[green]Model '{new_model_name}' loaded successfully!")
            return True
        except Exception as e:
            rich.print(Panel.fit(f"""[bold red](!) An error has occurred while loading the model.[/bold red]
[white]{e}""", border_style="bold red"))
            return False

    def list_models(self): # display list of pulled model using ollama list command
        try:
            response = self.client.list()
            models = getattr(response, "models", [])
            if not models:
                rich.print("[yellow]No models found on the connected server.[/yellow]")
                return
            for model in models:
                model_name = getattr(model, "model", getattr(model, "name", str(model)))
                rich.print(model_name)
            rich.print("\nTo view a list of models available for pull, visit https://ollama.com/search")
        except Exception as e:
            rich.print(Panel.fit(f"""[bold red](!) Unable to list models.[/bold red]
[white]{e}""", border_style="red"))

    def display_stats(self): # display stats for previous output
        try:
            rich.print("[bold]Stat for previous output")
            print(f"Model:             {self.modelin}")
            if self.response_time < 1000:
                print(f"Time:              {self.response_time:.2f} ms")
            else:
                t2 = round(self.response_time / 1000)
                print(f"Time:              ~ {t2:.2f} s ({self.response_time} ms)")
            print(f"Word count:        {self.word_count}")
            print(f"Raw response:      {self.is_raw}")
        
        except AttributeError:
            rich.print(Panel.fit("""[bold red](!) Unable to show stats[/bold red]
You may need to get a response atleast once.""", border_style="bold red"))
        except Exception as e:
            rich.print(Panel.fit(f"""[bold red](!) Unable to show stats[/bold red]
[white]{e}.""", border_style="bold red"))
    
    def rawouttoggle(self): # toggle setting to view non-formatted text
        if self.rawoutput == False: 
            self.rawoutput = True
            rich.print("[blue](i) Raw output is enabled")
        else: 
            self.rawoutput = False
            rich.print("[blue](i) Raw output is disabled")

    def refreshSet(self, speed): # set the refresh speed
        self.refreshSpeed = int(speed)
        rich.print(f"[blue](i) Refresh rate is now set to [bold white]{speed}")


    def _handle_command(self, user_input): # command handler
        cmd_parts = user_input.split(" ")
        command = cmd_parts[0]
        arg = cmd_parts[1] if len(cmd_parts) > 1 else None

        commands = {
            "/help": self.display_help,
            "/exit": self.exit_prog,
            "/list": self.list_models,
            "/clear": self.clear_output, 
            "/pull": lambda: self.pull_model(arg) if arg else rich.print("[bold red](!) Missing model name"),
            "/rm": lambda: self.remove_model(arg) if arg else rich.print("[bold red](!) Missing model name"),
            "/remove": lambda: self.remove_model(arg) if arg else rich.print("[bold red](!) Missing model name"),
            "/change": lambda: self.switch_model(arg) if arg else rich.print("[bold red](!) Missing model name"),
            "/stat": self.display_stats,
            "/about": self.about_prog,
            "/rawoutput": self.rawouttoggle,
            "/speed": lambda: self.refreshSet(arg) if arg else rich.print("[bold red](!) Missing integer"),
            "/file": lambda: self.read_file(),
            "/connect": lambda: self.network_access(arg) if arg else self.network_access(),
        }

        try:
            if command in commands:
                commands[command]()
            else:
                rich.print("[bold red](!) Unknown command.")
        except Exception as e:
            rich.print(Panel.fit(f"""[bold red](!) An error has occurred.[/bold red]
[white]{e}""", border_style="bold red"))


    def about_prog(self):
        rich.print(Panel.fit('''[bold blue]||||||||||||||||||||||||||| py-[/bold blue][bold yellow]ollama ||||||||||||||||||||||||||||[/bold yellow]
                             
[bold white][Version: 0.4dev][/bold white]
                             
A Python3-based terminal front-end interface for Ollama.
Made by: @bcahtechstuffs (https://github.com/bcahtechstuffs).

Modules used: ollama, rich, time, datetime, subprocess, os, sys.
All credits goes to each programmers for each Python modules.'''))


    def display_help(self):
        rich.print(Panel.fit('''[bold green]py-ollama commands (commands followed by underscore requires an additional argument):[/bold green]

/help              : Display list of available commands.
/exit              : Stop running LLMs then exit program.
/list              : List all pulled models. ('ollama list')
/clear             : Clear all previous outputs.
/pull _            : Pull an available LLM for using locally
/rm _ | /remove _  : Delete a pulled LLM from your drive.
/change _          : Switch to another model.
/stat              : Show statistics for previous response.
/about             : Show current version and credits.
/speed _           : Change output refresh rate.
/rawoutput         : Toggle to use markdown, panels on output.
/file              : Add file for current prompt (not toggle-able) (W.I.P)
/connect _         : Connect to an Ollama server, e.g. 192.168.1.50:11434, 127.0.0.1:11434.''', border_style="green"))

    def generate_chat_response(self, user_input): # TODO: fix jittering output when using rich.live (consider use different approach)
        try:
            rich.print(Panel.fit(f"[white]{user_input}", border_style="bold white"))
            if ":" in self.modelin:
                model_display_name = self.modelin.split(":")[0]
            else:
                model_display_name = self.modelin

            self.messages.append({'role': 'user', 'content': user_input})
            if self.fileReady:
                self.fileContent = "\n" + self.fileContent
                self.messages.append({'role': 'user', 'content': self.fileContent})
                self.fileReady = False
            
            self.word_count = 0
            self.is_raw = self.rawoutput
            start_time = time.time()
            assistant_response_content = ""
            rawcontent = ""
            current = Text()
            currentthink = Text()
            self.console.print(f"\n[blue]{model_display_name}:[/blue]")

            if not self.rawoutput: # potential bottleneck
                with Live(console=self.console, vertical_overflow="ellipsis", screen=False, refresh_per_second=self.refreshSpeed, transient=True) as lv:
                    rpanel = Panel.fit(
                        current,
                        border_style="blue"
                    )
                    tpanel = Panel.fit(
                        currentthink,
                        border_style="purple"
                    )
                    blankPanel = Panel("")
                    stream = self.client.chat(model=self.modelin, messages=self.messages, stream=True)
                    lv.update(rpanel)
                    is_thinking = False
                    for chunk in stream:
                        content = chunk['message']['content']
                        rawcontent += content
                        if content == "<think>" and not is_thinking:
                            is_thinking = True
                            lv.update(tpanel)
                        if content == "</think>" and is_thinking:
                            is_thinking = False
                            lv.update(rpanel)
                        if is_thinking:
                            currentthink.append(content)
                        else:  
                            current.append(content)
                        lv.update(rpanel if not is_thinking else tpanel)
                        if not is_thinking:
                            assistant_response_content += content
                        self.word_count += len(content.split())
                    lv.update(blankPanel)
                markdownc = Markdown(assistant_response_content)
                t = datetime.datetime.now()
                panel = Panel.fit(
                    markdownc,
                    border_style="white",
                    subtitle=str(f"[gray]{t.hour}:{t.minute:02d}:{t.second:02d}"),
                    subtitle_align="left",
                )
                self.console.print(panel)
            else:
                stream = self.client.chat(model=self.modelin, messages=self.messages, stream=True)
                for chunk in stream:
                    self.word_count += 1
                    print(chunk["message"]["content"], end="", flush=True)
                print("\n")
            # end of funni code

            end_time = time.time()
            self.response_time = (end_time - start_time) * 1000
            self.messages.append({'role': 'assistant', 'content': assistant_response_content})

        except Exception as e:
            rich.print(Panel.fit(f"""[bold red](!) An error has occurred during chat generation.
[white]{e}""", border_style="red"))
            self.exit_prog()
        finally:
            pass

    def start(self): # what u see when loading this program
        rich.print(Panel.fit("[bold blue]py-[bold yellow]ollama", border_style="blue"))
        rich.print(Panel.fit("""[bold white][Version : 0.4dev][/bold white]

[bold yellow]This is a development build, please do expect un-polished features[/bold yellow]
Please enter model name or a command below to start (or type [blue]`/help`[/blue] for list of commands):"""))
        if os.name != "nt":
            desktop_env = os.environ.get('XDG_CURRENT_DESKTOP')
            if not desktop_env:
                rich.print(Panel.fit("""[bold yellow](!) It looks like you're not using a desktop environment[/bold yellow]
                                     
[white]Fullscreen TTY may prevent you from scrolling up to read long LLM outputs.
It is recommended to use tmux on TTY or terminal emulators on desktop environment to read long outputs.""", border_style="yellow"))
        if (len(sys.argv)) > 1:
            model_input =  sys.argv[1]
            rich.print(f"Selected model: [bold white]{model_input}")
            if self.switch_model(model_input):
                rich.print("[white italic]Type [blue italic]/help[/blue italic] for list of commands.")
        else:
            while True:
                model_input = str(input("> ")).strip()
                if not model_input:
                    rich.print(Panel.fit("[bold red](x) No input", border_style="red"))
                    continue
                if model_input[0] == '/':
                    self._handle_command(model_input)
                    continue
                else:
                    if self.switch_model(model_input):
                        rich.print("[white italic]Type [blue italic]/help[/blue italic] for list of commands.")
                        break
                    else:
                        continue

        # main loop
        while True:
            user_input = self.console.input("[bold cyan]>>[/bold cyan] ")
            if not user_input:
                continue
            if user_input[0] == '/':
                self._handle_command(user_input)
            else:
                print("\033[A \033[K \033[A")
                self.generate_chat_response(user_input)

if __name__ == "__main__": # program starter
    print(" "*100, end="\r")
    app = pyollama()
    app.start()
