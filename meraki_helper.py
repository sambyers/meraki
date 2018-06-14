import requests
import json

api_url = "https://api.meraki.com/api/v0/"

def _get(api_endpoint, api_key):
    '''
    Generic get
    Return requests object.
    '''
    url = api_url + api_endpoint
    body = ""
    headers = {
        'content-type': "application/json",
        'x-cisco-meraki-api-key': api_key
        }

    try:
        response = requests.request("GET", url, data=body, headers=headers)
        if response.status_code >= 400:
            response.raise_for_status()
        return response
    except(NameError):
        print("The response is empty.")
        raise SystemExit
    except(ConnectionError):
        print("Missing or invalid connection argument (orgid, api_url, api_key).")
        raise SystemExit

def _put(api_endpoint, api_key, body):
    '''
    Generic put that takes dictionary as payload/body
    Return requests object.
    '''
    url = api_url + api_endpoint
    headers = {
        'content-type': "application/json",
        'x-cisco-meraki-api-key': api_key
        }
    #body = json.dumps(body)
    try:
        response = requests.request("PUT", url, json=body, headers=headers)
        if response.status_code >= 400:
            response.raise_for_status()
        return response
    except(ConnectionError):
        print("Missing or invalid connection argument (orgid, api_url, api_key).")
        raise SystemExit

def get_orgid(org_name, api_key):
    '''
    Get org id based on name given.
    Return string Organization name.
    '''
    api_endpoint = "organizations"
    response = _get(api_endpoint, api_key)
    try:
        json = response.json()
    except(ValueError):
        print("The json returned in the first response couldn't be decoded. Did you use your API key?")
        raise SystemExit

    for org in json:
        if org_name in (org['name']):
            return org['id']

def get_networkid(orgid, network_name, api_key):
    '''
    Get network id based on name given.
    Return string of network id.
    '''
    api_endpoint = "organizations/{0}/networks".format(orgid)
    response = _get(api_endpoint, api_key)
    json = response.json()

    for network in json:
        if network_name == (network['name']):
            return network['id']

def get_devices(network_id, api_key):
    '''
    Get all of the devices and their details in a network.
    Returns a list/dictionary of the json response.
    '''
    api_endpoint = "networks/{0}/devices".format(network_id)
    response = _get(api_endpoint, api_key)
    result = response.json()
    return result

def get_clients(serial, timespan, api_key):
    '''
    Get all of the devices and their details in a network.
    Returns a list/dictionary of the json response.
    '''
    api_endpoint = "devices/{0}/clients?timespan={1}".format(serial, timespan)
    response = _get(api_endpoint, api_key)
    result = response.json()
    return result

def get_vlans(network_id, api_key):
    '''
    Get all of the VLANs and their details in a network.
    Returns a list/dictionary of the json response.
    '''
    api_endpoint = "networks/{0}/vlans".format(network_id)
    response = _get(api_endpoint, api_key)
    result = response.json()
    return result

def get_vlan(network_id, api_key, vlan_id):
    '''
    Get a VLAN and its details.
    Returns a list/dictionary of the json response.
    '''
    api_endpoint = "networks/{0}/vlans/{1}".format(network_id, vlan_id)
    response = _get(api_endpoint, api_key)
    result = response.json()
    return result

def update_vlan(network_id, api_key, vlan_id, body):
    '''
    Update a VLAN subnet or name for a given network.
    Returns a list/dictionary of the json response.
    '''
    api_endpoint = "networks/{0}/vlans/{1}".format(network_id, vlan_id)
    response = _put(api_endpoint, api_key, body)
    return response

def update_client_group_policy(network_id, api_key, mac, body):
    '''
    Update a client group policy in a given network.
    Returns a list/dictionary of the json response.
    '''
    api_endpoint = "networks/{0}/clients/{1}/policy".format(network_id, mac)
    response = _put(api_endpoint, api_key, body)
    return response

def get_vlansubnets(network_id, api_key):
    '''
    Get the subnet information for each VLAN in the network.
    Returns a list of subnets.
    '''
    subnets = []
    vlans = get_vlans(network_id, api_key)
    for vlan in vlans:
        subnets.append(vlan['subnet'])
    return subnets

def get_staticroutes(network_id, api_key):
    '''
    Get all static routes and thheir details in a network.
    Return list/dictionary of the json response.
    '''
    api_endpoint = "networks/{0}/staticRoutes".format(network_id)
    response = _get(api_endpoint, api_key)
    json = response.json()
    return json

def get_staticsubnets(network_id, api_key):
    '''
    Get static routes and return only the subnet portion as a list.
    '''
    subnets = []
    routes = get_staticroutes(network_id, api_key)
    for route in routes:
        subnets.append(route['subnet'])
    return subnets
