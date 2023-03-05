import filecmp
import glob
import json
import os
from datetime import datetime


# get the most recent file added to the folder, if no file exists return null
def most_recent_file_from_audit():
    try:
        list_of_files = glob.glob('txtfiles/audittrail/*')  # * means all if need specific format then *.csv
        if list_of_files is None:
            return list_of_files
        else:
            latest_file = max(list_of_files, key=os.path.getctime)
            return latest_file
    except:
        return False


# get domaincheck.txt file from txtfiles folder
def get_current_file():
    currentfile = glob.glob('txtfiles/domaincheck.txt')
    return currentfile


# checks to see if there is an update to the file if so (Return: boolean value)
def check_for_updates():
    getmostrecentfile = most_recent_file_from_audit()
    get_current_file = "txtfiles/domaincheck.txt"
    if getmostrecentfile != "":
        boolean_value = comparelines(get_current_file, getmostrecentfile)
        return boolean_value


# overwrites the full details.
def updateFile(file, data):
    try:
        domaincheck = open(file, "a")
        domaincheck.write(str(data))
        domaincheck.close()
    except:
        pass


# copy paste the existing file
def Copy_paste_rename_file():
    timestamp = datetime.now()
    os.replace("txtfiles/json.loads(.json", "txtfiles/audittrail/domaincheck_" + timestamp + ".txt")


# open selected txt file, convert to python Dict (Return: Json) grab data as json
def open_file_retrieve_data(file):
    fileopened = open(file)
    fileopened = fileopened.read()
    converteddata = fileopened.replace("'", "\"")
    converteddata = converteddata.replace("\n", "")
    data = json.loads(converteddata)
    container = {'1': {}}
    currdictindex = int(container.__len__())
    if currdictindex == 1:
        container[str(currdictindex)].update(data)
    else:
        ++currdictindex
        container[str(currdictindex)].update(data)
    return container


# updates the file with the latest details
def updatearray(file, ipresults, socketResults, networkdeatils, timestamp, ipaddress, domain):
    for line in file:
        fileipaddress = line.get("ipaddress")
        filedomain = line.get("Domain")
        if fileipaddress == ipaddress or filedomain == domain:
            line.update({"ipaddress": ipresults, "socket Results": socketResults, "network details": networkdeatils,
                         "timestamp": timestamp})


# compare each line against File 1 and 2, if  (Return: True or False)
def comparelines(getmostrecentfile, get_current_file):
    f1 = open(getmostrecentfile)
    f2 = open(get_current_file)
    f1_data = f1.readlines()  # read file one
    f2_data = f2.readlines()  # read lines from file 2
    i = 0
    for line1 in f1_data:
        i += 1
        for line2 in f2_data:
            # matching line1 from both files
            if line1 == line2:
                None
            else:
                return False
                f1.close()
                f2.close()
                break
    # if all lines are the same return true
    return True
    # closing files
    f1.close()
    f2.close()