import tools, cli

subnet_finder = tools.subnet_finder()

TOOLS = {
    "sbnf": subnet_finder
    }

try:
    cli.run(TOOLS)
except EOFError:
    quit()