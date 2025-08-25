def run(tools, intro_shown=False):
    str = ""
    if not intro_shown:
        print("SUBNETTING TOOLS (q to quit)")
    
    while str != 'q':

        str = input("> ")

        str = str.lower()

        if str == 'q':
            return

        if str == "help" or str == "-h":
            print("Commands:")
            print("list, -l: Displays a list of available subnetting tools.")
            print("help, -l: The screen that is currently being shown.")
        elif str == "list" or str == "-l":
            for tool in tools:
                print(f"[{tool}] {tools[tool].name} - {tools[tool].description}")
        else:
            cmd = str.split()
            try:
                program = cmd.pop(0)
                if program in tools:
                    print(tools[program].exec(cmd))
                else:
                    print(f"Command {program} not found")
            except IndexError:
                continue
