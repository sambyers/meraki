# VLAN names and subet configuration
enterprise_networks = [
    {
        'network_name': 'Lab-test-hub1',
        'VLANS': [
            {'id': 128, 'name': 'Default', "applianceIp": "192.168.128.1", 'subnet': '192.168.128.0/24', "fixedIpAssignments": {},  "reservedIpRanges": [], "dnsNameservers": "opendns"}
        ]
    },
    {
        'network_name': 'Lab-test-spoke1',
        'VLANS': [
            {'id': 20, 'name': 'CDE', 'applianceIp': '172.16.20.1', 'subnet': '172.16.20.0/24', "dnsNameservers": "opendns"}
        ]
    }
]
