""" This Script for Qusery MS Sentinel by Sending Custom Searches for Enrichments and Threat Hunt Activities """
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

'''Sentinel KQL Search'''
SentinelSearch = 'KQL is here'

def Search_Sentinel(SentinelSearch):

    dataa = 'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}&resource=https://api.loganalytics.io'

    uri = 'https://login.microsoftonline.com/{tenant_id}/oauth2/token'

    ''' Post Request to get Authentication Basic Token '''
    response = requests.post(url=uri, data=dataa, verify=False)
    output = json.loads(response.text)
    Token = 'Bearer ' + output['access_token']
    
    ''' Send Post Request with KQL search '''
    uri1 = "https://api.loganalytics.io/v1/workspaces/{workspace_id}/query?query={}" .format(SentinelSearch)
    Headers = {"Authorization":Token, "Content-Type":"application/json"}
    
    response1 = requests.get(url=uri1, headers=Headers, verify=False)
    output = response1.text
    out=json.loads(output)

    context_data = []
    result = json.loads(response1.text)
    context = {
                'Sentinel': 'Result',
                'Tables': result
            }
    context_data.append(context)
    Table = tableToMarkdown('Tables', context_data, removeNull=True)
    entry = {
        'Type': entryTypes['note'],
        'Contents': context_data,
        'ContentsFormat': formats['json'],
        'ReadableContentsFormat': formats['markdown'],
        'HumanReadable': Table,
        'EntryContext': context
    }
    
    resturn entry