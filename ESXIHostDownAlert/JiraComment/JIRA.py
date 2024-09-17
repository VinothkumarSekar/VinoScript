
from jira import JIRA
#import csv


def handler (context, inputs):
    JIRA_username = inputs['JIRA_username']
    JIRA_password = inputs['JIRA_password']
    jsd_url= inputs['jsd_url']
    INTSD = inputs['INTSD']


    url = f'https://{jsd_url}'
    # Establish a connection to your Jira instance
    jira = JIRA(server=url, basic_auth=(JIRA_username, JIRA_password))

    # Define the Jira issue key


    issue = jira.issue(INTSD)
    assert issue
    labels = issue.fields.labels
    labels.append("Host_lost_connection_to_vc_automation")
    issue.update(fields={'labels': labels})



# # data rows as dictionary objects 
# mydict =[{'Name': 'Ash Ketchum', 'SNo': '1', 'Subject': 'English'}, 
#          {'Name': 'Gary Oak', 'SNo': '2', 'Subject': 'Mathematics'}, 
#          {'Name': 'Brock Lesner', 'SNo': '3', 'Subject': 'Physics'}]

# # field names 
# fields = ['SNo', 'Name', 'Subject'] 


# with open('/Users/vinoths/Desktop/SDDC Automation/vm_details.csv', 'w', newline='') as file: 
#     writer = csv.DictWriter(file, fieldnames = fields)

#     writer.writeheader() 

# # Specify the path to the CSV file you want to attach
# csv_file_path = 'vm_details.csv'

# # Open the CSV file in binary mode
# with open(csv_file_path, 'rb') as file:
#     # Attach the file to the Jira issue
#     jira.add_attachment(issue=issue_key, attachment=file)

# # Comment text to add
# comment_text = "Refer attachment named " + "*" + csv_file_path + "*" + " for VM details  " 

# comment_text += "||header1||header2||\n|one|two|"

# # Add a comment to Jira ticket
# jira.add_comment(issue=issue_key, body=comment_text)
