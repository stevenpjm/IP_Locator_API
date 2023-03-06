# Framework imports
import time, schedule
from datetime import datetime
import json
from dotenv import load_dotenv
import os

# project imports
from python import fileupdate, ipdomainrequest, checksubnetMask, socketcheck,pingip

#loads enviroment variables
# variables : domaincheck

def configure():
    load_dotenv()

def scheduleTasks():
    try:
        # Are the files different run the task
        fileupdate.check_for_updates()

        # current time stamp
        timestamp = datetime.now()

        # get ipaddress or domain from domain check file
        getdata = fileupdate.open_file_retrieve_data(os.getenv('domaincheck'))
        lastkey = list(getdata.keys())[-1]
        ipaddress = getdata[lastkey]["IP address"]

        if ipaddress != "":
            ipaddress = getdata[lastkey]["IP address"]
        else:
            ipaddress = getdata[lastkey]["domain"]


        # get ip address and mask prefix
        ipresults = ipdomainrequest.get_ip_details_from_domain(ipaddress)
        converteddata = ipresults.replace("'", "\"")
        converteddata = converteddata.replace("\n", "")
        data = json.loads(converteddata)
        ipaddress = data.get("network")
        position = len(ipaddress) - ipaddress.find("/")
        prefix = ipaddress[-abs(position):]
        ipaddress = ipaddress.replace(" ", "").rstrip(ipaddress[-abs(position):])

        # check socket
        socketResults = socketcheck.socketchecker(ipaddress)

        # get subnets, usable hosts,
        networkdetails = checksubnetMask.subnetmask(prefix)

        #ping ip address
        pingstatus = pingip.check_ping(ipaddress)

        # Creates file to audit trail
        file = fileupdate.Copy_paste_rename_file()

        # add results to file
        socketResults = str(socketResults)
        socketResults = socketResults.replace('/', '').replace('{', '').replace('}', '')
        domain = getdata[lastkey]["domain"]
        fileupdate.updatefilewithresults(file, domain, ipaddress, str(timestamp), str(networkdetails.get("prefix")), str(networkdetails.get("mask")), str(networkdetails.get("usablehost")), str(networkdetails.get("networkclass")), pingstatus, socketResults )

        # Has the file been updated
        updatedfile = "Yes"

        # Update last run task
        lastrun = "{'Date':" + str(timestamp) + ", 'Triggered': 'scheduled','Updated':" + updatedfile + "}"
        fileupdate.updateFile(os.getenv('lastrun'), lastrun)


    except:
        return "error with running tasks please consult the admin"