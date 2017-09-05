 
from meraki_helper import get_args, get_orgid, get_networkid, get_vlansubnets, get_staticsubnets

# To do:
# - Add csv export

def main():

    api_url = "https://dashboard.meraki.com/api/v0/"

    # Collect args from user
    args = get_args()
    api_key = args.key
    org_name = args.org
    network_name = args.net

    # Grab the org id and network id based on the named provided.
    org_id = get_orgid(org_name, api_url, api_key)
    network_id = get_networkid(org_id, network_name, api_url, api_key)

    # Grad all subnets that are configured on VLANs and as static routes.
    vlan_subnets = get_vlansubnets(network_id, api_url, api_key)
    static_routes_subnets = get_staticsubnets(network_id, api_url, api_key)
    
    # Concatenate the two subnet lists.
    subnets = vlan_subnets + static_routes_subnets
    print(subnets)

    with open('networks.txt', 'w') as f:
        f.write("\n".join(subnets))

if __name__ == '__main__':
    main()