import requests
import ssl
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import re


requests.packages.urllib3.disable_warnings()


vcenter_host = 'xxx-vc-xxx.com'
vcenter_user = 'xxx'
vcenter_password = 'xxx'
Affected_host = 'xxxe.com'


def get_vcenter_session():
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE
    si = SmartConnect(host=vcenter_host, 
                        user=vcenter_user,
                        pwd=vcenter_password, 
                        port=443, 
                        sslContext=context)
    return si


def get_esxi_hosts(content):
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
    return container.view


def get_esxi_sensor_status(esxi_host):
    sensor_status = []
    for sensor in esxi_host.runtime.healthSystemRuntime.systemHealthInfo.numericSensorInfo:
            # if re.search('.+Temp.+', sensor.healthState.key) :
            if (sensor.healthState.key == 'Green') and sensor.sensorType == "temperature": 
                sensor_status.append({
                    'Sensor': sensor.name,
                    'Status': sensor.healthState.key,
                    'CurrentReading': sensor.currentReading,
                    'baseUnit': sensor.baseUnits
                    
                })
 
    return sensor_status


content = get_vcenter_session().RetrieveContent()

esxi_hosts = get_esxi_hosts(content)
body = ""
for esxi_host in esxi_hosts:
    if esxi_host.name == Affected_host:
        print()
        #print('Report from ESXi Host:', esxi_host.name)
        header = f'Report from ESXi Host: {esxi_host.name}'
        print(header)
        sensor_status = get_esxi_sensor_status(esxi_host)
        if sensor_status == []:
             #print("All the sensors are green")
             body = "All the sensors are green"
        else:     
            for sensor in sensor_status:
                senName = sensor['Sensor'] 
                senStatus = sensor['Status']
                senBaseUnit = sensor['baseUnit']
                senCurrentReading = sensor['CurrentReading']
                senCurrentReading = str(senCurrentReading)[:2]

                #print (f' {senName} is in state: {senStatus}')
                body += f'{senName} is in state: {senStatus}' + '\n'
                body += f'With reading {senCurrentReading} {senBaseUnit}' + '\n' '\n'

        print (body)        
            # print('Sensor:', sensor['Sensor'])
            # print('Status:', sensor['Status'])
        print()



Disconnect(get_vcenter_session())

