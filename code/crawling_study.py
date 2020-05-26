import req as req
from slacker import Slacker
from konlpy.tag import Okt
import time

import requests as req
from bs4 import BeautifulSoup as bfs

def dining_code(q):
    params = {
        'query': q
    }
    # 응답 get 요청
    html = req.get('http://www.diningcode.com/list.php?', params=params).text

    soup = bfs(html, 'html.parser')
    rank_list = []

    # 1위 ~10위 식당이름하고, 링크
    # print(enumerate(soup.select('span.btxt'), 1))
    for idx, tag in enumerate(soup.select('span.btxt'), 1):
        rank_list.append('{}'.format(tag.text))

    return rank_list

#test2.py
def notification(message):
    token = 'xoxb-445422292193-447426542310-hpnHoRJsiKKn2XA8Ud8USU00'
    slack = Slacker(token)
    slack.chat.post_message('#general', message)


from slackclient import SlackClient
slack_token = 'xoxb-445422292193-447426542310-hpnHoRJsiKKn2XA8Ud8USU00'
sc = SlackClient( slack_token )

if sc.rtm_connect():
    while True:
        receive_data = sc.rtm_read()
        if len( receive_data ):
            keys = list( receive_data[0].keys() )
            if 'type' in keys and 'text' in keys and 'user' in keys:
                print( receive_data[0] )
                message = receive_data[0]['text']
                spliter = Okt()
                nouns = spliter.nouns(message)
                result = ""
                for i in nouns:
                    print(i)
                    result = result + i + "+"
                print(result)
                print(dining_code(result))
                for i in [1,2,3,4,5]:
                    notification(dining_code(result)[i])
        time.sleep(1)

else:
    print("connection Failed")
