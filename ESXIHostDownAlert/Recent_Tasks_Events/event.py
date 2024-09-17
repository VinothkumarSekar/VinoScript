from datetime import datetime, timedelta
import ssl
from pyVim.connect import SmartConnect
from pyVmomi import vim
import pytz
import csv
import tempfile
from re import search


def time_obj():
    time_filter = vim.event.EventFilterSpec.ByTime()
    now = datetime.now(tz=pytz.utc)
    time_filter.beginTime = now - timedelta(minutes=120)
    time_filter.endTime = now
    return time_filter

def entity_obj():
    event_type_list = []
    host = vim.HostSystem('host-1022')
    byEntity = vim.event.EventFilterSpec.ByEntity(entity=host, recursion="self")
    filter_spec = vim.event.EventFilterSpec(eventTypeId=event_type_list, time=time_obj(), entity=byEntity)
    return filter_spec

def main():
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE
    si = SmartConnect(host="xxx-vc04.oc.xxx.com", user="administrator@vsphere.local",
                      pwd="xxx", sslContext=context)
    current_time = si.CurrentTime()
    eventManager = si.content.eventManager
    # root_folder = si.content.rootFolder

    event_collector = eventManager.CreateCollectorForEvents(entity_obj())
    page_size = 1000  # The default and also the max event number per page till vSphere v6.5, you can change it to a smaller value by SetCollectorPageSize().
    events = []
    # while True:
    # If there's a huge number of events in the expected time range, this while loop will take a while.
    events_in_page = event_collector.ReadNextEvents(page_size)
    num_event_in_page = len(events_in_page)
    # if num_event_in_page == 0:
    events_dict = {}
    events_list = []
    des_list = []
    for event in events_in_page:
        events_dict['description'] = event.fullFormattedMessage
        events_dict['time'] = event.createdTime
        events_dict['target'] = event.host.name
        events_dict['user'] = event.userName
        events_list.append(events_dict)

        des_list.append(event.fullFormattedMessage)

    update_csv(events_list)
    # des = des_list.Task 
    # print(des)

       



def update_csv(events_list):
    csv_headers = ['Description', 'Time', 'Target', 'User']
    # with tempfile.TemporaryDirectory() as tmpdirname:
    #     print('created temporary directory', tmpdirname)
    #     csv_file = f"{tmpdirname}/event_details.csv"
    with open("event_details.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_headers)
        for event in events_list:
            writer.writerow([event['description'], event['time'].strftime("%Y-%m-%d %H:%M:%S"), event['target'], event['user']])



if __name__ == '__main__':
    main()
