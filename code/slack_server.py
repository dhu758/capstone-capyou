from slacker import Slacker
import time

def notification(message):
    token = 'xoxp-446035951986-447395041574-446054335922-d2670381ae1ce28310d472b7da53c8f3'
    slack = Slacker(token)
    slack.chat.post_message('#capston', message)

#RTM
from slackclient import SlackClient

slack_token = 'xoxp-446035951986-447395041574-446054335922-d2670381ae1ce28310d472b7da53c8f3'
sc = SlackClient(slack_token)

if sc.rtm_connect():
    while True:
        receive_data = sc.rtm_read()

        if len(receive_data):
            keys = list(receive_data[0].keys())
            if 'type' in keys and 'text' in keys and 'user' in keys:
                print(receive_data[0])
                message = receive_data[0]['text']
                notification('두 번 따라하는 앵무새 :'+ message +' '+ message)

        time.sleep(1)

else :
    print("connection Failed")
