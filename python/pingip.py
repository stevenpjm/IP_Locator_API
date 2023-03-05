import os

def check_ping(ipaddress):
    response = os.system("ping -c 1 " + ipaddress)
    # and then check the response...
    if response == 0:
        pingstatus = "Network Active"
    else:
        pingstatus = "Network Error"
    return pingstatus