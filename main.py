import tools, cli, tomllib

subnet_information = tools.subnet_information()

TOOLS = {
    subnet_information.abbreviation: subnet_information
    }

try:
    cli.run(TOOLS)
except EOFError:
    quit()