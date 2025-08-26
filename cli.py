def run(tools, intro_shown=False):
    str = ""
    if not intro_shown:
        print("SUBNETTING TOOLS (q to quit)")
    
    while str != 'q':

        str = input("> ").lower()

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
                    # If only program is specified, enter program exec mode
                    if len(cmd) == 0:
                        print(f"[{program}] EXEC mode (q to quit)")
                        while cmd != ['q']:
                            cmd = input(f"[{program}] ").lower().split()
                            print(tools[program].exec(cmd))
                    else:
                        print(tools[program].exec(cmd))
                else:
                    print(f"Command {program} not found")
            except IndexError:
                continue