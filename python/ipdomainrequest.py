import requests
from dotenv import load_dotenv
import socket
import os


# create the envir variable
def configure():
    load_dotenv()


def get_ip_details_from_domain(ipordomain):
    try:

        if ".com" or ".org" in ipordomain:
            ipordomain = socket.gethostbyname(ipordomain)

            url = os.getenv('url')
            querystring = {"ip": ipordomain, "apikey": os.getenv('queryapi')}
            headers = {
                "X-RapidAPI-Key": os.getenv('api_key'),
                "X-RapidAPI-Host": "find-any-ip-address-or-domain-location-world-wide.p.rapidapi.com"
            }
            # request to make the url endpoint
            response = requests.request("GET", url, headers=headers, params=querystring)
            # if there is error in the response this will display back to the user
            if response.status_code == 403:
                return "There was an error in your request : " + response.content.decode()
            else:
                return response.text

    # this handles any errors in the python framework
    except Exception as err:
        return f"Unexpected {err=}, {type(err)=}"
