# meraki
Repo for scripts written for Meraki
- **Get started**
  - Install [Python](https://www.python.org/)
  - Install [git](https://git-scm.com/)
  - ```git clone https://github.com/sambyers/meraki```
  - ```pip install -r requirements.txt```
- **get-all-subnets**: Gets all subnets across a network either configured on a VLAN interface or as a static route. Helps with IP planning! You need an API key, the organization, and the network. The script prints the networks and writes them to a txt file.
- **update_vlans**: Updates VLANs based on a configuration file. Useful for post template corrections or variations.
- **gpmod**: Updates Group Policy on devices based on the gpconfig file.
