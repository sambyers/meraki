# meraki
Repo for scripts written for Meraki
- **Get started**
  - Install [Python](https://www.python.org/)
  - Install [git](https://git-scm.com/)
  - ```git clone https://github.com/sambyers/meraki```
  - ```pip install -r requirements.txt```
- **get-all-subnets.py**: Gets all subnets across a network either configured on a VLAN interface or as a static route. Helps with IP planning! You need an API key, the organization, and the network. The script prints the networks and writes them to a txt file.  
```usage: get-all-subnets.py [-h] [-k KEY] [-o ORG] [-n NET]```
- **update_vlans.py**: Updates VLANs based on a configuration file.  
```usage: get-all-subnets.py [-h] [-k KEY] [-o ORG] [-n NET]```
