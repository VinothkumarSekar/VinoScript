import slack

class SlackPost:
  def __init__(self, channel_id, message, client, message_ts):
    self.channel_id = channel_id
    self.message = message
    self.client = client
    self.message_ts = message_ts

  def thread_message_slack(self):
    try:
        response = self.client.chat_postMessage(channel=self.channel_id, text=self.message , thread_ts=self.message_ts)
  
    except slack.errors.SlackApiError as e:
        print(f"Error sending message: {e}")
        return None



def handler(context, inputs):

        channel_id = inputs['channel_id']
        slack_bot_token = inputs['slack_bot_token']
        message1 = inputs['message1']
        message2 = inputs['message2']
        message_ts = inputs['message_ts']
        message3 = f"\n ```{inputs['message3']}```"


        if 'successful' in message1:
            message = message1 + message2
        elif 'failed' in message1:
             message = message1 + message2 + message3


        client = slack.WebClient(token=slack_bot_token)
        slack_obj = SlackPost(channel_id, message, client, message_ts)
        slack_obj.thread_message_slack()

        
print(handler(inputs))
