# py-ollama: alternative front-end for ollama
# version 0.3
# finally, stable release

try:
    import rich
    from rich.panel import Panel
    from rich.live import Live
    from rich.text import Text
    from rich.markdown import Markdown
    rich.print("[italic]Starting py-ollama...", end="\r")
except ModuleNotFoundError:
    print("(x) Missing dependencies")
    print("Your Python install is missing rich module which is required for displaying formatted output.")
    print("You can install them by running `python3 -m pip install -r requirements.txt` within py-ollama folder.")
    exit()

try:
    import ollama, os, time, subprocess, datetime
except ModuleNotFoundError as e:
    rich.print("[bold red](x) Missing dependencies")
    rich.print(f"[red]{e}")
    rich.print("[white]Your Python install is missing module(s) which are [white bold]required[/white bold] for py-ollama's functions.")
    rich.print("[white]You can install them by running `python3 -m pip install -r requirements.txt` within py-ollama folder.")
    exit()

class pyollama: # one big chunk of code
    def __init__(self):
        self.client = ollama.Client()
        self.modelin = ""
        self.messages = []
        self.word_count = 0
        self.response_time = 0
        self.console = rich.console.Console()
        self.rawoutput = False

    def exit_prog(self):
        rich.print("[italic]Exiting...")
        if self.modelin:
            subprocess.run(["ollama", "stop", self.modelin], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.name == 'nt':
            subprocess.run(['taskkill', '/f', '/im', 'ollama'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(["killall", "ollama"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        exit()

    def clear_output(self):
        if os.name == 'nt':
            os.system("cls")
        else:
            os.system("clear")
        self.messages = []

    def pull_model(self, model_name):
        rich.print(f'[italic]Pulling [white italic]{model_name}...[/white italic]')
        os.system(f'ollama pull {model_name}')

    def remove_model(self, model_name):
        rich.print(f'[italic]Removing [white italic]{model_name}...[/white italic]')
        os.system(f'ollama rm {model_name}')

    def switch_model(self, new_model_name):
        subprocess.run(["ollama", "stop", self.modelin], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        rich.print(f"[italic]Loading [white bold]{new_model_name}[/white bold]...")
        try:
            self.client.chat(model=new_model_name, messages=[{'role': 'user', 'content': "hi"}])
            self.modelin = new_model_name
            rich.print(f"[green]Model '{new_model_name}' loaded successfully!")
            return True
        except Exception as e:
            rich.print("[bold red](!) An error has occurred while loading the model.")
            rich.print(f"[red]{e}")
            return False

    def list_models(self):
        os.system('ollama list')
        rich.print("\nTo view a list of models available for pull, visit https://ollama.com/search")

    def display_stats(self):
        rich.print("[bold]Stat for previous output")
        print(f"Model:             {self.modelin}")
        if self.response_time < 1000:
            print(f"Time:              {self.response_time:.2f} ms")
        else:
            t2 = round(self.response_time / 1000)
            print(f"Time:              {self.response_time:.2f} ms (~{t2} s)")
        print(f"Word count:        {self.word_count}")
        print(f"Is raw response:   {self.is_raw}")
    
    def rawouttoggle(self):
        if self.rawoutput == False: 
            self.rawoutput = True
            rich.print("[blue](i) Raw output is enabled")
        else: 
            self.rawoutput = False
            rich.print("[blue](i) Raw output is disabled")

    

    def _handle_command(self, user_input):
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
            "/change": lambda: self.switch_model(arg) if arg else rich.print("[bold red](!) Missing model name"),
            "/stat": self.display_stats,
            "/rawoutput": self.rawouttoggle,
            "/about": self.about_prog
        }

        try:
            if command in commands:
                commands[command]()
            else:
                rich.print("[bold red](!) Unknown command.")
        except Exception as e:
            rich.print("[bold red](!) An error has occurred")
            rich.print(f"[red]{e}")
            self.exit_prog()
    def about_prog(self):
        rich.print(Panel.fit(Markdown('''**py-ollama**\n
**[Version: 0.3 - June 12 '25]**\n
A Python3-based terminal front-end interface for Ollama\n
Progammed by: [@bcahtechstuffs](https://github.com/bcahtechstuffs)\n
Modules used: ollama, rich, time, datetime, subprocess''')))


    def display_help(self):
        """Displays available commands."""
        print('''py-ollama commands (commands followed by underscore requires an additional argument):
/help   : Display list of available commands
/exit   : Stop running LLMs then exit program.
/list   : List all pulled models. ('ollama list')
/clear  : Clear all previous outputs.
/pull _ : Pull an available LLM for using locally ('ollama pull')
/rm _   : Delete a pulled LLM from your drive. ('ollama rm')
/change _: Switch to another model.
/stat   : Show statistics for previous response.
/about  : Show credits. (although only one single dude made this code)
        ''')

    def generate_chat_response(self, user_input): # TODO: fix jittering output when using rich.live
        try:
            if ":" in self.modelin:
                model_display_name = self.modelin.split(":")[0]
            else:
                model_display_name = self.modelin

            self.messages.append({'role': 'user', 'content': user_input})
            self.word_count = 0
            self.is_raw = self.rawoutput
            start_time = time.time()
            assistant_response_content = ""
            rawcontent = ""
            current = Text()
            currentthink = Text()
            self.console.print(f"\n[blue]{model_display_name}:[/blue]")
            if not self.rawoutput:
                with Live(console=self.console, vertical_overflow="ellipsis", screen=False, refresh_per_second=5, transient=True) as lv:
                    rpanel = Panel.fit(
                        current,
                        border_style="blue"
                    )
                    tpanel = Panel.fit(
                        currentthink,
                        border_style="purple"
                    )
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
                    print(chunk["message"]["content"], end="", flush=True)
                print("\n")

            end_time = time.time()
            self.response_time = (end_time - start_time) * 1000
            self.messages.append({'role': 'assistant', 'content': assistant_response_content})

        except Exception as e:
            rich.print("[bold red](!) An error has occurred during chat generation.")
            rich.print(f"[red]{e}")
            self.exit_prog()
        finally:
            pass

    def start(self):
        rich.print(Panel.fit("[bold blue]py-[bold yellow]ollama", border_style="blue"))
        rich.print(Panel.fit("""[bold white][Version: 0.3][/bold white]

A Python3-based terminal front-end interface for Ollama.
Please enter model name below to start (or type [blue]`/help`[/blue] for list of commands):"""))

        while True:
            model_input = str(input("> ")).strip()
            if not model_input:
                rich.print("[bold red](x) No input")
                continue
            if model_input[0] == '/':
                self._handle_command(model_input)
                continue
            else:
                rich.print(f"Selected model: [bold white]{model_input}")
                if self.switch_model(model_input):
                    rich.print("[white italic]Type [blue italic]/help[/blue italic] for list of commands.")
                    break
                else:
                    continue

        # Main chat loop
        while True:
            user_input = self.console.input("[bold cyan]>>[/bold cyan] ")
            if not user_input:
                continue
            if user_input[0] == '/':
                self._handle_command(user_input)
            else:
                self.generate_chat_response(user_input)

if __name__ == "__main__": # program starter
    print(" "*100, end="\r")
    app = pyollama()
    app.start()
