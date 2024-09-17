
from jira import JIRA
def handler(context, inputs):
    JIRA_username = inputs["jira_user"]
    JIRA_password = inputs["jira_pwd"]

# Establish a connection to your Jira instance
    jira = JIRA(server='https://servicedesk.xxxx.com', basic_auth=(JIRA_username, JIRA_password))

# Define the Jira issue key
    issue_key = inputs["JIRA"]

    mydict =[{'Name': 'Ash Ketchum', 'SNo': '1', 'Subject': 'English'}, 
         {'Name': 'Gary Oak', 'SNo': '2', 'Subject': 'Mathematics'}, 
         {'Name': 'Brock Lesner', 'SNo': '3', 'Subject': 'Physics'}]

# field names 
    fields = ['SNo', 'Name', 'Subject'] 

    with open('vm_details.csv', 'w', newline='') as file: 
        writer = csv.DictWriter(file, fieldnames = fields)

        writer.writeheader() 

# Specify the path to the CSV file you want to attach
    csv_file_path = 'vm_details.csv'

# Open the CSV file in binary mode
    with open(csv_file_path, 'rb') as file:
    # Attach the file to the Jira issue
        jira.add_attachment(issue=issue_key, attachment=file)

# Comment text to add
    comment_text = "Refer attachment named " + "*" + csv_file_path + "*" + " for VM details  " 

# Add a comment to Jira ticket
    jira.add_comment(issue=issue_key, body=comment_text)
