''' NSX Python Code aims to Connect to VMware NSX and update Specific Virtual Machine tags '''
             ''' This integration is developed by Osama Elsherbiny ''' 
        ''' Linkedin: https://www.linkedin.com/in/osama-elsherbiny-a92386152/ '''
        
import json
from typing import Any, Dict, Tuple, List, Optional, Union, cast
import requests


''' NSX Parameters '''
nsx_manager = 'NSX Host Here!'
nsx_api_user = 'Put User Here!'
nsx_api_password = 'Put Password Here!'
external_id = 'Put the target VM external id here!'

nsx_session_create = '/api/session/create'
nsx_post_tag = '/api/v1/fabric/virtual-machines?action=add_tags'
nsx_update_config = '/api/v1/csm/virtual-machines?action=update_config'
nsx_update_tags = '/api/v1/fabric/virtual-machines?action=update_tags'
update_config_url = '/api/v1/csm/virtual-machines?action=update_config'


def nsx_update_tag(external_id):
    user= nsx_api_user
    user_password= nsx_api_password
    nsx_auth_url= 'https://{nsx_manager}{nsx_session_create}'
    auth_header = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    auth_body = f"j_username={user}&j_password={user_password}"
    session = requests.session()
    session.verify = False
    session.headers = auth_header
    
    ''' Send Post request to create Session and get XSRF token and cookies '''
    response = session.post(nsx_auth_url, data=auth_body)
    Json_token = response.headers['Set-Cookie'][0:43]
    XSRF_Token = response.headers['X-XSRF-TOKEN']
    #print(Json_token)
    #print(XSRF_Token)
    
    ''' Set XSRF Token and Cookies in request headers '''
    session_header = {'X-XSRF-TOKEN': f"{XSRF_Token}",'Content-Type': 'application/json', 'Cookie':f"{Json_token}"}
    nsx_session = requests.session()
    nsx_session.verify = False
    nsx_session.headers = session_header
    nsx_session.cookies = Json_token
    headers = session_header
    cookies = Json_token
    
    if nsx_session.headers and nsx_session.cookies != None:
        print(response.status_code)
        print("Authentication Success")
    else:
        print(response.status_code)
        print("Authentication Failed")


    ''' Get Certain VM tags by its external id '''
    response = session.get(f"https://{nsx_manager}/api/v1/fabric/virtual-machines?external_id={external_id}", headers=session_header, verify=False)
    print('-------Fetching Current VM Details-----------')
    print(response.status_code)

    print("Checking if there is old tags")
    tagresult = json.loads(response.text)
    tags = []
    if "tags" in tagresult['results'][0]:
        print("Found Old Tags related to VM")
        print(tagresult['results'][0]['tags'])
        tags = tagresult['results'][0]['tags']
    else:
        print("No Old tags found")
    old_tags = tags

    ''' Apend the new tags to the old tags array to be used further on update request '''
    new_tags = {"scope": "ransomware", "tag": "isolate"}
    old_tags.append(new_tags)
    dataa = {"external_id": external_id,"tags": old_tags} # New tags & Old tags


    ''' Send Post request to update certain VM tags by its external id '''
    response = session.post(f"https://{nsx_manager}/api/v1/fabric/virtual-machines?action=update_tags",json=dataa, headers=session_header, verify=False)
    print('-------Updating VM Tag-----------')
    print(response.status_code)


    if response.status_code == 204:
        x = "Vm tag was updated Successfully"
        results = {'result': x}
    else:
        y = "VM tag wasn't updated"
        results = {'result': y}

    return results