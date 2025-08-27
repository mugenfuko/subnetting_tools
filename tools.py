import modules, tomllib

def read_config_file(filepath, key=""):
    try:
        with open(filepath, "rb") as f:
            data = tomllib.load(f)
        if key in data.keys():
            return data[key]
    except FileNotFoundError:
        return

class subnet_information:
    name = "Subnet Information"
    abbreviation = "sbni"
    description = "A tool to find various information about a given subnet."
    usage = f"usage: {abbreviation} [IPV4 ADDRESS] [SUBNETMASK]\nrand, -r: Script generates random ip/mask and executes"
    default_config = {"show_broadcast_address" : True}

    rand = False

    def exec(self, cmd):

        # Load config, use default config in case of error
        # TODO autogenerate config file if none present
        config = read_config_file("config.toml", self.abbreviation)
        if not config:
            config = self.default_config

        NETMASK_VALUES = modules.generate_netmask_values()

        def parse_cmd(cmd):

            data = {}
            if cmd == []:
                data["msg"] = "Missing IP address and netmask"
                return data
            
            if cmd[0] == 'q':
                data["msg"] = "Session terminated"

            if cmd[0] == "help" or cmd[0] == "-h":
                data["msg"] = f"{self.name} - {self.description}\n{self.usage}"

            # Super secret command for testing purposes
            if cmd[0] == "rand" or cmd[0] == "-r":
                data["msg"] = "rand"
            
            if "msg" not in data.keys():
                if len(cmd) < 2:
                    data["msg"] = "Missing IP address or netmask"
                    return data

                if modules.is_ipv4_address(cmd[0]):
                    data["address"] = cmd[0].split('.')
                else:
                    data["msg"] = f"{cmd[0]} is not a valid IPv4 address"
                    return data

                if modules.is_netmask(cmd[1]):
                    data["netmask"] = cmd[1].split('.')
                else:
                    data["msg"] = f"{cmd[1]} is not a valid netmask"
                    return data
            return data

        def find_relevant_index(nm):
            i = 0
            while i < len(nm)-1:
                if int(nm[i]) < 255:
                    break
                i += 1
            return i
        
        # Find first or final network value depending on parameter
        def find_network_values(ad, nm, find="first"):
            # Retrieve index of octet to process
            index = find_relevant_index(nm)
            ad_octet = int(ad[index])
            nm_octet = int(nm[index])
            # Calculate remainder of addresses
            remainder = 256 - nm_octet
            # Calculate how many times the remainder fits
            times_fits = ad_octet // remainder
            # Calculate value of network octet
            first_network_value = remainder * times_fits
            if find == "last":
                return (first_network_value - 1) + remainder
            else:
                return first_network_value

        # Generate subnetwork addresses based on given network value and filler (0 or 255 in practice)
        def generate_subnet_address(ad, nm, nv, filler="0"):
            subnet_address = []
            # Retrieve index of octet to process
            index = find_relevant_index(nm)
            for i, octet in enumerate(ad):
                # Leave prior octets as is
                if i < index:
                    subnet_address.append(octet)
                # Insert network value in relevant octet
                elif i == index:
                    subnet_address.append(str(nv))
                # Insert filler in remaining octets
                else:
                    subnet_address.append(filler)
            return subnet_address

        data = parse_cmd(cmd)
        if "msg" in data.keys() and data["msg"] != "rand": # For randomization, might remove later
            return f"[{self.abbreviation}] {data["msg"]}"
        else:

            # Below lines for randomization, might remove later
            if "msg" in data.keys() and data["msg"] == "rand":
                data["address"] = modules.generate_random_ip()
                data["netmask"] = modules.generate_random_netmask()
                print(f"(rand) {'.'.join(data["address"])} {'.'.join(data["netmask"])}")

            # Normal lines start here
            raw = {}
            first_network_value = find_network_values(data["address"], data["netmask"])
            # Generate subnet address
            raw["subnet address"] = '.'.join(generate_subnet_address(data["address"], data["netmask"], first_network_value))
            # Generate broadcast address
            if config["show_broadcast_address"] == True:
                last_network_value = find_network_values(data["address"], data["netmask"], "last")
                raw["broadcast address"] = '.'.join(generate_subnet_address(data["address"], data["netmask"], last_network_value, "255"))
            
            # Make the raw look nnnice~
            output = []
            for k, v in raw.items():
                output.append(f"{k}: {v}")
            return f"[{self.abbreviation}]\n{'\n'.join(output)}"