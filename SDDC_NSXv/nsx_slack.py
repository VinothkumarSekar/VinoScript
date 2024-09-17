import slack
import json

class SlackPost:
  def __init__(self, channel_id, message, message4, client, attachment_colour, attachment_json):
    self.channel_id = channel_id
    self.message = message
    self.client = client
    self.message4 = message4
    self.attachment_colour = attachment_colour
    self.attachment_json = attachment_json
    self.message_ts = None
    self.thread_attachment_json = None

    thread_attachment = [
            {
                "color": self.attachment_colour,
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": self.message4
                        }
                    }
                ]
            }
        ]
    
    self.thread_attachment_json = json.dumps(thread_attachment) 
 

  def message_slack(self):
    try:
        response = self.client.chat_postMessage(channel=self.channel_id, attachments=self.attachment_json)
        self.message_ts = response['ts']
        return response["ts"]
    except slack.errors.SlackApiError as e:
        print(f"Error sending message: {e}")
        return None

  def reply_in_thread(self):
    try:
        response = self.client.chat_postMessage(channel=self.channel_id,attachments=self.thread_attachment_json,thread_ts=self.message_ts)
        return response["ok"]
    except SlackApiError as e:
        print(f"Error replying to message: {e}")
        return None

def handler(context,inputs):

        INTSD = inputs['INTSD']
        channel_id = inputs['channel_id']
        slack_bot_token = inputs['slack_bot_token']
        message1 = inputs['message1']
        message2 = '<' +  'https://servicedesk.xxxx/browse/' + inputs['INTSD']+'|' + inputs['INTSD']+',' '>'
        message3 = inputs["hostName"]
        message4 = f"\n ```{inputs['workflow_comment']}```"
        attachment_colour = inputs['attachment_colour']
        try:
          message = message1 + message2 + " " + message3
          attachment = [
            {
                "color": attachment_colour,
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": message
                        }
                    }
                ]
            }
            ]
    
          attachment_json = json.dumps(attachment)
          
        except TypeError:
          message = message1 + message2
          attachment = [
            {
                "color": attachment_colour,
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": message
                        }
                    }
                ]
            }
            ]
    
          attachment_json = json.dumps(attachment)
        client = slack.WebClient(token=slack_bot_token)
        slack_obj = SlackPost(channel_id, message, message4, client, attachment_colour, attachment_json)
        slack_obj.message_slack()
        slack_obj.reply_in_thread()

inputs = {
        'INTSD' : 'INTSD',
        'channel_id' : "C03MZ592xxx",
        'slack_bot_token' : "x",
        'message1' : " <!channel> NSXv Controller Validation ",
        'hostName' : 'hostName',
        'workflow_comment' : "actual comment / exception",
        'attachment_colour' : "#44BD7D"

       
    }
handler(inputs)
