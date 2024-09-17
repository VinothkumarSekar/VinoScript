
import slack
from slack.errors import SlackApiError
import json


class slack_post:
  def __init__(self, channel_id, message, client, reply_txt, attachment_colour):
    self.channel_id = channel_id
    self.message = message
    self.client = client
    self.reply_txt = reply_txt
    self.attachment_colour = attachment_colour
    self.message_ts = None
    self.attachment_json = None



    attachment = [
                {
                    "color": self.attachment_colour,
                    "blocks": [
                      {
                        "type": "section",
                        "text": {
                          "type": "plain_text",

                          "text": "Status from workflow:"
                        }
                      },
                      {
                        "type": "divider"
                      },
                      {
                        "type": "divider"
                      },
                      {
                        "type": "section",
                        "text": {
                          "type": "mrkdwn",
                          "text": "*workflow is completed:*"
                        }
                      },
                      {
                        "type": "section",
                        "text": {
                          "type": "mrkdwn",
                          "text": "Click on the button to see logs."
                        },
                        "accessory": {
                          "type": "button",
                          "text": {
                            "type": "plain_text",
                            "text": "Click Me",
                          },
                          "value": "pressed",
                          "action_id": "workflow logs"
                        }
                      }
                    ]
                  }
                
        ]
    
    self.attachment_json = json.dumps(attachment) 

  def message_slack(self):
    try:
        response = self.client.chat_postMessage(channel=self.channel_id, attachments=self.attachment_json)
        self.message_ts = response['ts']
        return response["ts"]  
    except SlackApiError as e:
        print(f"Error sending message: {e}")
        return None
    
  def reply_in_thread(self):
    try:
        response = self.client.chat_postMessage(channel=self.channel_id,text=self.reply_txt,thread_ts=self.message_ts)
        return response["ok"] 
    except SlackApiError as e:
        print(f"Error replying to message: {e}")
        return None  
    
    

inputs = {
        'INTSD' : 'JIRA-123456',
        'channel_id' : "C03MZ5xxx",
        'message1' : "Test message from bot ",
        'slack_bot_token' : "x",
        'attach_text' : 'File attachement in thread',
        'reply_text' : "Reply test to the initial message as thread!"

    }


def handler(inputs):

        INTSD = inputs['INTSD']
        channel_id = inputs['channel_id']
        message1 = inputs['message1']
        slack_bot_token = inputs['slack_bot_token']
        reply_text = f"\n```{inputs['reply_text']}```"
        message2 = '<' +  'https://servicedesk.xxx.com/browse/' + inputs['INTSD']+'|' + inputs['INTSD']+ '>'
        message = message1 + message2 
        attachment_colour = "#36a64f"

    
        reply_txt = reply_text

        



        client = slack.WebClient(token=slack_bot_token)
        slack_obj = slack_post(channel_id, message, client, reply_txt, attachment_colour)
        message_ts = slack_obj.message_slack()

        if message_ts:
            reply_ts = slack_obj.reply_in_thread()
            if reply_ts:
                print("Reply sent successfully!")



handler(inputs)
