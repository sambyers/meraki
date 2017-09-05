import requests
import argparse

# To do
# - Class-ify this collection of functions

def get_args():
    '''
    Get args from CLI.
    '''
    parser = argparse.ArgumentParser(description="Get arguments for script.")
    parser.add_argument('-k', '--key', type=str, help="API Key for Meraki.")
    parser.add_argument('-o', '--org', type=str, help="Organization name.")
    parser.add_argument('-n', '--net', type=str, help="Network name.")
    parser.add_argument('-csv', action="store_true", help="Export network list as csv.")

    args = parser.parse_args()
    return args


def _get(api_endpoint, api_url, api_key):
    '''
    Generic get
    Return requests object.
    '''
    url = api_url + api_endpoint
    payload = ""
    headers = {
        'content-type': "application/json",
        'x-cisco-meraki-api-key': api_key
        }

    try:
        response = requests.request("GET", url, data=payload, headers=headers)
        return response
    except(NameError):
        print("The response is empty.")
        raise SystemExit


def get_orgid(org_name, api_url, api_key):
    '''
    Get org id based on name given.
    Return string Organization name.
    '''
    api_endpoint = "organizations"
    response = _get(api_endpoint, api_url, api_key)
    try:
        json = response.json()
    except(ValueError):
        print("The json returned in the first response couldn't be decoded. Did you use your API key?")
        raise SystemExit

    for org in json:
        if org_name in (org['name']):
            return org['id']


def get_networkid(orgid, network_name, api_url, api_key):
    '''
    Get network id based on name given.
    Return string of network id.
    '''
    api_endpoint = "organizations/{0}/networks".format(orgid)
    response = _get(api_endpoint, api_url, api_key)
    json = response.json()
    
    for network in json:
        if network_name == (network['name']):
            return network['id']


def get_vlans(network_id, api_url, api_key):
    '''
    Get all of the VLANs and their details in a network.
    Returns a list/dictionary of the json response.
    '''
    api_endpoint = "networks/{0}/vlans".format(network_id)
    response = _get(api_endpoint, api_url, api_key)
    json = response.json()
    return json


def get_vlansubnets(network_id, api_url, api_key):
    '''
    Get the subnet information for each VLAN in the network.
    Returns a list of subnets.
    '''

    subnets = []
    vlans = get_vlans(network_id, api_url, api_key)
    for vlan in vlans:
        subnets.append(vlan['subnet'])
    return subnets


def get_staticroutes(network_id, api_url, api_key):
    '''
    Get all static routes and thheir details in a network.
    Return list/dictionary of the json response.
    '''
    api_endpoint = "networks/{0}/staticRoutes".format(network_id)
    response = _get(api_endpoint, api_url, api_key)
    json = response.json()
    return json


def get_staticsubnets(network_id, api_url, api_key):
    '''
    Get static routes and return only the subnet portion as a list.
    '''
    subnets = []
    routes = get_staticroutes(network_id, api_url, api_key)
    for route in routes:
        subnets.append(route['subnet'])
    return subnets

