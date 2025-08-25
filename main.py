import tools, cli

sbntfndr = tools.subnet_finder()

TOOLS = {
    "sbnf": sbntfndr
    }

try:
    cli.run(TOOLS)
    #tools.subnet_finder.exec(sbntfndr, ["DEBUG"])
except EOFError:
    quit()
