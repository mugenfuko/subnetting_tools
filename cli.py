def run(tools, intro_shown=False):
    output = ""
    if not intro_shown:
        print("***SUBNETTING TOOLS***")
    str = input("> ")

    str = str.lower()

    if str == "help" or str == "-h":
        print("List of commands:")
        print("list, -l: Displays a list of available subnetting tools.")

    if str == "list" or str == "-l":
        for tool in tools:
            print(f"[{tool}] {tools[tool].name} - {tools[tool].description}")

    cmd = str.split()
    try:
        program = cmd.pop(0)
        if program in tools:
            output = tools[program].exec(cmd)
    except IndexError:
        # Optional toggle to keep program running if input can't be recognized
        #run(tools, True)
        return

    print(output)
