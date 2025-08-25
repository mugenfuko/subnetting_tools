import modules

class subnet_finder:
    name = "Subnet Finder"
    description = "A tool to find the network address of a given subnet."
    usage = "usage: sbnf [IPV4 ADDRESS] [SUBNETMASK]"

    def exec(self, cmd):

        NETMASK_VALUES = modules.netmask_values

        data = {
            "address" : "",
            "netmask" : "",
        }

        def parse_cmd(cmd):

            if cmd[0] == "help" or cmd[0] == "-h":
                return f"{self.name} - {self.description}\n{self.usage}"
            
            if len(cmd) < 2:
                return "Missing IP address or netmask!"

            if is_ipv4_address(cmd[0]):
                data["address"] = cmd[0].split('.')
            else:
                return f"{cmd[0]} is not a valid IPv4 address."

            if is_netmask(cmd[1]):
                data["netmask"] = cmd[1].split('.')
            else:
                return f"{cmd[1]} is not a valid netmask."

        def is_integer(str):
            try:
                str = float(str)
            except ValueError:
                return False
            return True

        def is_ipv4_address(str):
            # Check if address has 3 dots
            if str.count('.') != 3:
                return False
            
            # Convert to array if there are 3 dots
            arr = str.split('.')
            
            for n in arr:
                # Check if each variable in array is integer
                if not is_integer(n):
                    return False
                # Check if each variable in array is 0-255
                if int(n) < 0 or int(n) > 255:
                    return False
            return True
        
        def is_netmask(str):
            # Check if IPv4 address format
            if not is_ipv4_address(str):
                return False
            arr = str.split('.')
            for i, n in enumerate(arr):
                n = int(n)
                # Check if values are possible netmask values
                if n not in NETMASK_VALUES:
                    return False
                    break
                if i > 0:
                    # Check for logical sequencing of netmask
                    prev = int(arr[i-1])
                    if n > 0 and prev != 255:
                        return False
                        break
                    if n > prev:
                        return False
                        break
            return True

        def find_relevant_index(mask):
            for i, octet in enumerate(mask):
                if int(octet) < 255:
                    return i
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

        # For testing purposes
        data["address"] = modules.random_ip
        data["netmask"] = modules.random_netmask

        # Disabled for testing purposes
        #output = parse_cmd(cmd)
        if data["address"] and data["netmask"]:
            output = f"IPv4 Address: {'.'.join(data["address"])}\nSubnet mask: {'.'.join(data["netmask"])}".split('\n')

            print(f"Address: {data["address"]}")
            print(f"Netmask: {data["netmask"]}")
            print(find_network_value(data["address"], data["netmask"]))
            # TO DO: Write function that can generate a network address from network_value
            # TO DO: Write function that can generate a broadcast address

        return output