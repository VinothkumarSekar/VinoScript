
# vcd_url = "https://vcd05.xxx.com/api"
# username = "xxxx"
# password = "xxxx"
# org_name = "vcd04-xxxx-sandbox-t"
# template_name = "QA CentOS Test"
# vm_name = "vinoths-testVM"
# vCloud Director API endpoint

from pyvcloud.vcd.client import BasicLoginCredentials, Client
from pyvcloud.vcd.vm import VM
from pyvcloud.vcd.vdc import VDC

# Disable SSL certificate verification (for development/testing purposes only)
import requests
requests.packages.urllib3.disable_warnings()

# vCloud Director API details
vcd_host = 'vcd05xxx.com'
username = 'xxx'
password = 'xxx'
org_name = 'vcd04-xxx-sandbox-t'
vdc_name = 'vcd04-xxx-sandbox-t-ovdc1'
template_name = 'QA CentOS Test'
vm_name = 'vinoths-testVM'

# Create the vCloud Director API client
client = Client(vcd_host, verify_ssl_certs=False)
credentials = BasicLoginCredentials(username, org_name, password)
client.set_credentials(credentials)

# Retrieve the VDC (Virtual Data Center)
org_resource = client.get_org()
vdc_resource = client.get_vdc(org_resource, vdc_name)
vdc = VDC(client, resource=vdc_resource)

# Retrieve the template
template = vdc.get_vapp_template(template_name)

# Create a VM from the template
vm = VM(client, vdc=vdc_resource)
result = vm.instantiate_vapp(template, name=vm_name)

# Print the result
print('VM deployed successfully:', result)
