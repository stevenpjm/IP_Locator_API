import json

def subnetmask(prefix):
    try:
        fileopened = open("txtfiles/subnet.txt","r")
        fileopened = fileopened.read()
        converteddata = fileopened.replace("'", "\"")
        converteddata = converteddata.replace("\n", "")
        data = json.loads(converteddata)

        # loop through subnetclass.txt file to get subnet mask
        for line in data:
            if data[line]["Prefix size"] == prefix:
                prefix = data[line]["Prefix size"]
                mask = data[line]["Network mask"]
                usablehosts = data[line]["Usable hosts"]
                networkclass = data[line]["Class"]
                dataResults = {"prefix": prefix, "mask": mask, "usable hosts": usablehosts, "network class": networkclass}
                break
        return dataResults

    except:
        return "issue with subnetmask"
