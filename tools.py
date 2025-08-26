import modules

class subnet_finder:
    name = "Subnet Finder"
    description = "A tool to find the network address of a given subnet."
    usage = "usage: sbnf [IPV4 ADDRESS] [SUBNETMASK]\nrand, -r: Script generates random ip/mask and executes"

    def exec(self, cmd):

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
                random_ip = modules.generate_random_ip()
                random_netmask = modules.generate_random_netmask()
                data["msg"] = f"(RAND)IP{random_ip} (RAND)MASK{random_netmask}\nSUBNET: {'.'.join(generate_subnet_address(random_ip, random_netmask, find_network_value(random_ip, random_netmask)))}"
            
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

        def find_relevant_index(mask):
            i = 0
            while i < len(mask):
                if int(mask[i]) < 255:
                    break
                i += 1
            return i
        
        def find_network_value(ad, nm):
            # Retrieve index of octet to process
            index = find_relevant_index(nm)
            ad_octet = int(ad[index])
            nm_octet = int(nm[index])
            # Calculate remainder of addresses
            remainder = 256 - nm_octet
            # Calculate how many times the remainder fits
            times_fits = ad_octet // remainder
            # Calculate value of network octet
            network_value = remainder * times_fits
            return network_value

        def generate_subnet_address(ad, nm, nv):
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
                # Insert zeroes in remaining octets
                else:
                    subnet_address.append("0")
            return subnet_address

        data = parse_cmd(cmd)
        if "msg" in data.keys():
            return f"[sbnf] {data["msg"]}"
        else:
            subnet_address = generate_subnet_address(data["address"], data["netmask"], find_network_value(data["address"], data["netmask"]))
            return f"[sbnf] SUBNET: {'.'.join(subnet_address)}"