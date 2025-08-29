import modules, tomllib

def read_config(filepath, key=""):
    try:
        with open(filepath, "rb") as f:
            data = tomllib.load(f)
        if key in data.keys():
            return data[key]
    except FileNotFoundError:
        return

# Fix spelling errors and the like in the config file
def merge_configs(config, default):
    # If a key isn't in the config file, supplement with key/value from default config
    for key in default.keys():
        if key not in config.keys():
            print(f"Key \"{key}\" not present in config file, reverting to default")
            config[key] = default[key]
    return config

class subnet_information:
    name = "Subnet Information"
    abbreviation = "sbni"
    description = "A tool to find various information about a given subnet."
    usage = f"usage: {abbreviation} [IPV4 ADDRESS] [SUBNETMASK]\nrand, -r: Script generates random ip/mask and executes"
    default_config = {
        "show_broadcast_address" : True,
        "show_first_host_address" : True,
        "show_last_host_address" : True
        }

    def exec(self, cmd):

        # Load and merge config, use default config in case of error
        # TODO autogenerate config file if none present
        config = merge_configs(read_config("config.toml", self.abbreviation), self.default_config)
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

            # Not so secret command for testing purposes
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
        def find_first_or_last_network_value(ad, nm, first=True):
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
            if not first:
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

        def generate_broadcast_address(ad, nm):
            last_network_value = find_first_or_last_network_value(ad, nm, False)
            return generate_subnet_address(ad, nm, last_network_value, "255")

        def generate_first_or_last_host_address(ad, first=True):
            # TODO Handle edge cases like /31 or /32 prefix length            
            i = len(ad) - 1
            while i >= 0:
                if first and ad[i] != "255":
                    ad[i] = str(int(ad[i]) + 1)
                    break
                elif not first and ad[i] != "0":
                    ad[i] = str(int(ad[i]) - 1)
                    break
                i -= 1
            print(ad)
            return ad

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
            address = data["address"]
            netmask = data["netmask"]
            raw = {}

            # Generate subnet address
            first_network_value = find_first_or_last_network_value(address, netmask, True)
            raw["subnet address"] = '.'.join(generate_subnet_address(address, netmask, first_network_value))
            # Generate broadcast address
            if config["show_broadcast_address"]:
                raw["broadcast address"] = '.'.join(generate_broadcast_address(address, netmask))
            
            # First host address
            if config["show_first_host_address"]:
                raw["first host address"] = '.'.join(generate_first_or_last_host_address(raw["subnet address"].split('.')))
            
            # Last host address
            if config["show_last_host_address"]:
                raw["last host address"] = '.'.join(generate_first_or_last_host_address(generate_broadcast_address(address, netmask), False))

            # Make the raw look nnnice~
            output = []
            for k, v in raw.items():
                output.append(f"{k}: {v}")
            return f"[{self.abbreviation}]\n{'\n'.join(output)}"