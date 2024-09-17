import requests


# Replace the following placeholders with your vCenter Server details
vcenter_name = "xxx-vc24.xxx.com"
username = "xx"
password = "xx"

# Construct the API endpoint URL
url = f"https://{vcenter_name}/rest/vcenter/host/maintenance"

# Create a session
session = requests.Session()

# Authenticate with the vCenter Server
session.post(f"https://{vcenter_name}/api/session", auth=(username, password))

# Get the task details
tasks_response = session.get(f"{url}/task")
tasks_data = tasks_response.json()

# Get the event details
events_response = session.get(f"{url}/event")
events_data = events_response.json()

# Process and print the task details
print("Host Maintenance Mode Tasks:")
for task in tasks_data["value"]:
    print("Task ID:", task["task"])
    print("Status:", task["status"])
    print("Start Time:", task["start_time"])
    print("End Time:", task["end_time"])
    print("-" * 20)

# Process and print the event details
print("Host Maintenance Mode Events:")
for event in events_data["value"]:
    print("Event ID:", event["event"])
    print("Created Time:", event["created_time"])
    print("Event Type:", event["event_type"])
    print("Message:", event["message"])
    print("-" * 20)

# Logout from the session
session.delete(f"https://{vcenter_name}/api/session")
