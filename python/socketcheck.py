import socket


# verifies if the socket is open
def socketchecker(ipaddress):
    ipsocketreport = set({})
    port_number = ["8080"]  # Ports to check
    for port in port_number:

        try:
            # setups the type of socket to check
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            port = int(port)
            ipaddress = ipaddress.replace('\'', "\"")
            # connects to ip and port
            s.connect((ipaddress, port))
            errorString = ipaddress + " on Port : " + str(port) + " Connected"
            ipsocketreport.add(errorString)
            s.shutdown(2)

        except socket.error as e:
            errorString = ipaddress + " on Port : " + str(port) + " failed to connect"
            ipsocketreport.add(errorString)

    return ipsocketreport
