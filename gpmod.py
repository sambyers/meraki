
from meraki_helper import get_orgid, get_networkid, get_devices, get_clients, update_client_group_policy
import gpconfig
import argparse

def get_args():
    '''
    Get args from CLI.
    '''
    parser = argparse.ArgumentParser(description="Get arguments for script.")
    parser.add_argument('-k', '--key', type=str, help="API Key for Meraki.")
    parser.add_argument('-o', '--org', type=str, help="Organization name.")
    parser.add_argument('-n', '--net', type=str, help="Network name.")

    args = parser.parse_args()
    return args

def main():

    api_url = "https://dashboard.meraki.com/api/v0/"

    # Collect args from user
    args = get_args()
    api_key = args.key
    org_name = args.org
    network_name = args.net

    # Grab the org id and network id based on the names provided.
    org_id = get_orgid(org_name, api_key)
    network_id = get_networkid(org_id, network_name, api_key)
    devices = get_devices(network_id, api_key)
    
    for device in devices:
        clients = get_clients(device['serial'], '7200', api_key)
        if clients:
            for client in clients:
                mac = client['mac']
                if mac in gpconfig.client_gp_config:
                    payload = {"mac":mac,"type":"Group policy","groupPolicyId":gpconfig.client_gp_config[mac]}
                    result = update_client_group_policy(network_id, api_key, mac, payload)
                    print(result)
                else:
                    print("No clients to update in this network.")
        else:
            print("No clients on this device: {0} - {1}.".format(device['serial'],device['model']))

if __name__ == '__main__':
    main()
