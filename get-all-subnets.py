import requests
import argparse

api_url = "https://dashboard.meraki.com/api/v0/"
api_key = "4008d11a8c0f3" #For demonstration only. Not a real API key.


def get_args():
    '''
    Get args from CLI.
    '''
    parser = argparse.ArgumentParser(description="Get arguments for script.")
    parser.add_argument('-o', '--org', type=str, help="Organization name.")
    parser.add_argument('-n', '--net', type=str, help="Network name.")
    parser.add_argument('-csv', action="store_true", help="Export network list as csv.")

    args = parser.parse_args()
    return args

def _get(api_endpoint, api_url=api_url, api_key=api_key):
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


def get_orgid(org_name):
    '''
    Get org id based on name given.
    Return string Organization name.
    '''
    api_endpoint = "organizations"
    response = _get(api_endpoint)
    json = response.json()

    for org in json:
        if org_name in (org['name']):
            return org['id']


def get_networkid(orgid, network_name):
    '''
    Get network id based on name given.
    Return string of network id.
    '''
    api_endpoint = "organizations/{0}/networks".format(orgid)
    response = _get(api_endpoint)
    json = response.json()
    
    for network in json:
        if network_name == (network['name']):
            return network['id']


def get_vlans(network_id):
    '''
    Get all of the VLANs and their details in a network.
    Returns a list/dictionary of the json response.
    '''
    api_endpoint = "networks/{0}/vlans".format(network_id)
    response = _get(api_endpoint)
    json = response.json()
    return json


def get_vlansubnets(network_id):
    '''
    Get the subnet information for each VLAN in the network.
    Returns a list of subnets.
    '''

    subnets = []
    vlans = get_vlans(network_id)
    for vlan in vlans:
        subnets.append(vlan['subnet'])
    return subnets


def get_staticroutes(network_id):
    '''
    Get all static routes and thheir details in a network.
    Return list/dictionary of the json response.
    '''
    api_endpoint = "networks/{0}/staticRoutes".format(network_id)
    response = _get(api_endpoint)
    json = response.json()
    return json


def get_staticsubnets(network_id):
    '''
    Get static routes and return only the subnet portion as a list.
    '''
    subnets = []
    routes = get_staticroutes(network_id)
    for route in routes:
        subnets.append(route['subnet'])
    return subnets    


def main():

    # Collect args from user
    args = get_args()
    org_name = args.org
    network_name = args.net

    # Grab the org id and network id based on the named provided.
    org_id = get_orgid(org_name)
    network_id = get_networkid(org_id, network_name)

    # Grad all subnets that are configured on VLANs and as static routes.
    vlan_subnets = get_vlansubnets(network_id)
    static_routes_subnets = get_staticsubnets(network_id)
    
    # Concatenate the two subnet lists.
    subnets = vlan_subnets + static_routes_subnets
    print(subnets)

if __name__ == '__main__':
    main()