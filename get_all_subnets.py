
from meraki_helper import get_orgid, get_networkid, get_vlansubnets, get_staticsubnets
import argparse
# To do:
# - Add csv export

def get_args():
    '''
    Get args from CLI.
    '''
    parser = argparse.ArgumentParser(description="Get arguments for script.")
    parser.add_argument('-k', '--key', type=str, help="API Key for Meraki.")
    parser.add_argument('-o', '--org', type=str, help="Organization name.")
    parser.add_argument('-n', '--net', type=str, help="Network name.")
    parser.add_argument('-t', action="store_true", help="Export network list as text file.")

    args = parser.parse_args()
    return args

def main():

    api_url = "https://dashboard.meraki.com/api/v0/"

    # Collect args from user
    args = get_args()
    api_key = args.key
    org_name = args.org
    network_name = args.net
    text_export = args.t

    # Grab the org id and network id based on the names provided.
    org_id = get_orgid(org_name, api_url, api_key)
    network_id = get_networkid(org_id, network_name, api_url, api_key)

    # Grab all subnets that are configured on VLANs and as static routes.
    vlan_subnets = get_vlansubnets(network_id, api_url, api_key)
    static_routes_subnets = get_staticsubnets(network_id, api_url, api_key)

    # Concatenate the two subnet lists.
    subnets = vlan_subnets + static_routes_subnets
    print(subnets)

    if text_export:
        with open('networks.txt', 'w') as f:
            f.write("\n".join(subnets))
        print("Exported text file with networks.")

if __name__ == '__main__':
    main()
