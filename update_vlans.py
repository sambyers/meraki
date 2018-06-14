
from meraki_helper import get_orgid, get_networkid, get_vlans, update_vlan, get_vlan
import enterprise_vlan_configuration
import argparse

def get_args():
    '''
    Get args from CLI.
    '''
    parser = argparse.ArgumentParser(description="Get arguments for script.")
    parser.add_argument('-k', '--key', type=str, help="API Key for Meraki.")
    parser.add_argument('-o', '--org', type=str, help="Organization name.")

    args = parser.parse_args()
    return args

def main():

    api_url = "https://dashboard.meraki.com/api/v0/"

    # Collect args from user
    args = get_args()
    api_key = args.key
    org_name = args.org

    # Grab the org id and network id based on the names provided.
    org_id = get_orgid(org_name, api_url, api_key)

    for network in enterprise_vlan_configuration.enterprise_networks:
        network_id = get_networkid(org_id, network['network_name'], api_url, api_key)
        dashboard_vlans = get_vlans(network_id, api_url, api_key)

        for config_vlan in network['VLANS']:
            for dashboard_vlan in dashboard_vlans:
                if dashboard_vlan['id'] == config_vlan['id'] and dashboard_vlan['name'] == config_vlan['name'] and dashboard_vlan['subnet'] == config_vlan['subnet']:
                    print("The {0} network is configured as defined in your VLAN configuration file.".format(network['network_name']))

                elif dashboard_vlan['id'] == config_vlan['id']:
                    vlan_id = config_vlan.pop('id')
                    result = update_vlan(network_id, api_url, api_key, vlan_id, config_vlan)
                    if result.status_code == 200:
                        result = get_vlan(network_id, api_url, api_key, vlan_id)
                        print("The {0} network was not configured as defined in your VLAN configuration file. It has been updated.".format(network['network_name']))
                        print("Resulting VLAN config:")
                        print("VLAN ID: {0}, Name: {1}, Subnet: {2}, Appliance IP: {3}".format(result['id'],
                                                                                                result['name'],
                                                                                                result['subnet'],
                                                                                                result['applianceIp']))
                else:
                    print("Nothing matched.")

if __name__ == '__main__':
    main()
