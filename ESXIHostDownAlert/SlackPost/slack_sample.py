import json
from slack_bolt import App

class send_slack_message():

    def run(self, **kwargs):        
        slack_token = kwargs['slack_token']         
        slack_channel_name = kwargs['slack_channel_name']
        slack_channel_id = kwargs['slack_channel_id']
        thread_ts = kwargs['thread_ts']
        text_message = kwargs['text_message']
        attachment_colour = kwargs['attachment_colour']
        block_text = kwargs['block_text']
        message_type = kwargs['message_type']
        username = kwargs['username']
        user_icon = kwargs['user_icon']
        slack = App(token=slack_token)
        
        attachment_json = None

        if block_text != None:
            if attachment_colour == None:
                attach_colour = "#999999"
            else:
                attach_colour = attachment_colour

            attachment = [
                        {
                            "color": attach_colour,
                            "blocks": [
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": block_text
                                    }
                                }
                            ]
                        }
                    ]
        
            attachment_json = json.dumps(attachment) 
        
        try:
            if message_type == 'create':
                post_new = slack.client.chat_postMessage(channel=slack_channel_name, text=text_message, attachments=attachment_json, username=username, icon_emoji=user_icon)
                # print(post_new['channel'])
                # print(post_new['ts'])
                thread_ts = post_new['ts']
                channel_id = post_new['channel']
                create_new_output = {
                    'channel_id' : channel_id,
                    'message_ts' : thread_ts
                }
                return create_new_output
            elif message_type == 'reply':
                post_new = slack.client.chat_postMessage(channel=slack_channel_name,username=username, text=text_message, thread_ts=thread_ts, attachments=attachment_json, icon_emoji=user_icon)
                thread_ts = post_new['ts']
                channel_id = post_new['channel']
                reply_output = {
                    'channel_id' : channel_id,
                    'message_ts' : thread_ts
                }
                return reply_output
            elif message_type == 'update':
                post_new = slack.client.chat_update(channel=slack_channel_id, text=text_message, ts=thread_ts, attachments=attachment_json)
                thread_ts = post_new['ts']
                channel_id = post_new['channel']
                update_message_output = {
                    'channel_id' : channel_id,
                    'message_ts' : thread_ts
                }
                return update_message_output                                  

        except Exception as e:
            print(f"An error occurred trying to create slack message status. Error: {e}")

def handler(context, inputs):
    jsonOut = json.dumps(inputs, separators=(',', ':'))
    all_input_dict = json.loads(jsonOut)

    input_data = {}
    input_data.update(all_input_dict)

    config_data = {}
    config_data.update(all_input_dict)

    slack_connect = send_slack_message()
    slack_connect.config = config_data
    send_slack_message_status = slack_connect.run(**input_data)

    outputs = {
      "status": "done",
      "results": send_slack_message_status
    }
    print(outputs)
    return outputs
