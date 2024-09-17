import os
import slack
from pathlib import Path
from dotenv import load_dotenv
from slack.errors import SlackApiError

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)



client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])


def message_slack(channel_id, message):
    try:
        response = client.chat_postMessage(channel=channel_id, text=message)
        return response["ts"]  
    except SlackApiError as e:
        print(f"Error sending message: {e}")
        return None
    
def reply_in_thread(channel_id, message_ts, reply_text):
    try:
        response = client.chat_postMessage(channel=channel_id,text=reply_text,thread_ts=message_ts)
        return response["ok"] 
    except SlackApiError as e:
        print(f"Error replying to message: {e}")
        return None
def attach_in_thread(channel_id, message_ts, attach_text, file_name):
    try:
        response = client.files_upload(channels=channel_id,initial_comment=attach_text,thread_ts=message_ts,file=file_name)
        return response["ok"] 
    except SlackApiError as e:
        print(f"Error attaching to message: {e}")
        return None


if __name__ == "__main__":

    JIRA = "JIRA-238212"
    channel_id = "C03Mxxx"
    message = f" <!channel> Workflow has been initiated for hostDown alert <https://servicedesk.xxx.com/browse/{JIRA}|{JIRA}>  "
    file_name = "/Users/vinoths/Downloads/event_details-23.csv"
    SLACK_BOT_TOKEN = "xoxb-*************-8CiSA"
    
    message_ts = message_slack(channel_id, message)

    if message_ts:
        reply_text = "Reply test to the initial message as thread!"
        reply_ts = reply_in_thread(channel_id, message_ts, reply_text)
        if reply_ts:
            print("Reply sent successfully!")
            

    if message_ts:
        attach_text = "File attachement in thread"
        attach_ts = attach_in_thread (channel_id, message_ts, attach_text, file_name)
        if attach_ts:
            print("File attached successfully to slack thread!")

    




# File attach to slack 
# file_name = "/Users/vinoths/Downloads/event_details-23.csv"

# result = client.files_upload(
#     channels=channel_id,
#     initial_comment="Find attachment for ESXi tasks&events",
#     file=file_name,
# )



#client = slack.WebClient(token=SLACK_BOT_TOKEN)
#client = slack.WebClient(token=os.environ['SLACK_DEV_BOT_TOKEN'])
#client.chat_postMessage(channel='#vcc-sddc-automation' , text = " @here python slack msg test from devbot!! ")


#===== to run web server 
# from flask import Flask
# from slackeventsapi import SlackEventAdapter
#slack_event_adaptor = SlackEventAdapter(os.environ['SLACK_DEV_BOT_SIGN'],'/slack/events',app)

# app = Flask(__name__)
# if __name__ == "__main__":
#     app.run(debug=True)
