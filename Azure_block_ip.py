""" This Script for automating one of the eradication action by blocking client ip address on azure identity and access management """
             ''' This integration is developed by Osama Elsherbiny ''' 
        ''' Linkedin: https://www.linkedin.com/in/osama-elsherbiny-a92386152/ '''

import json
from typing import Any, Dict, Tuple, List, Optional, Union, cast
import requests

''' Sentinel Credentials '''
client_id = 'Client ID Here!'
client_secret = 'Client Secret Here!'
tenant_id = 'Tenant ID Here!'
workspace_id = 'Workspace ID Here!'
namedlocation_listID = 'Put the ID for where the IP will be added to Here!' #ID of blocking list

ipaddress = "10.10.1.100"

def ip_command(ipaddress):
    
    ''' Request Data & URL '''
    auth_data = 'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}&resource=https://graph.microsoft.com'
    auth_uri = 'https://login.microsoftonline.com/{tenant_id}/oauth2/token'
    
    ''' Post Request to get Authentication Basic Token '''
    response = requests.post(url=auth_uri, data=auth_data, verify=False)
    output = json.loads(response.text)
    Token = 'Bearer ' + output['access_token']

    ''' Get the content of the Ipnamed list of IPs '''
    IPList_uri = 'https://graph.microsoft.com/v1.0/identity/conditionalAccess/namedLocations/{namedlocation_listID}'
    req_headers = {"Authorization":Token, "Content-Type":"application/json"}
    response2 = requests.get(url=IPList_uri, headers=req_headers)


    resp = json.loads(response2.text)
    ipnamed_content = resp['ipRanges']
    #print("____________________________")
    ipnamed_content2 = str(ipnamed_content).replace('[','').replace(']','')
    old_ips = ipnamed_content2.replace("u", '')
    old_ips3 = old_ips.replace("'",'"')

    NewIP = ipaddress
    NewIP = {"@odata.type": "#microsoft.graph.iPv4CidrRange", "cidrAddress": NewIP}
    old = old_ips3
    New = []
    ''' Append the new IPs to the old Ip list '''
    ipnamed_content.append(NewIP)
    print(ipnamed_content)

    Update_blockList = {
        "@odata.type": "#microsoft.graph.ipNamedLocation",
        "displayName": "CSOC - blocked IPs",
        "isTrusted": False,
        "ipRanges": ipnamed_content
    }

    ''' Update the blocking list with the new Ip list '''
    response3 = requests.patch(url=IPList_uri, json=Update_blockList, headers=req_headers, verify=False)
    print("This is the content/body of new Ipnamed List " + response3.text)
    response3 = requests.get(url=IPList_uri, headers=req_headers)

    result = {
                'Ok': response3.status_code,
                'Output': response3.text
    }
    
    resturn result


