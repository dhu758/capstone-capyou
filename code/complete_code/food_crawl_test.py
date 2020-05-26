# 유림 구현연습

import req as req
from slacker import Slacker
# from konlpy.tag import Okt
import time

import folium
from selenium import webdriver

import requests as req
from bs4 import BeautifulSoup as bfs

token = 'xoxb-445422292193-447426542310-hpnHoRJsiKKn2XA8Ud8USU00'
slack = Slacker(token)

def notification(message):
    # token = 'xoxb-445422292193-447426542310-hpnHoRJsiKKn2XA8Ud8USU00'
    # slack = Slacker(token)
    slack.chat.post_message('#general', message)

def notification2(attachments):
    # token = 'xoxb-445422292193-447426542310-hpnHoRJsiKKn2XA8Ud8USU00'
    # slack = Slacker(token)
    slack.chat.post_message('#general', text=None, attachments=attachments)

from slackclient import SlackClient
# slack_token = 'xoxb-445422292193-447426542310-hpnHoRJsiKKn2XA8Ud8USU00'
sc = SlackClient( token )
# sc = SlackClient( slack_token )


def dining_code(q):
    params = {
        'query': q
    }
    # 응답 get 요청
    html = req.get('http://www.diningcode.com/list.php?', params=params).text

    soup = bfs(html, 'html.parser')
    rank_list = [] # 1~10 index에 맛집 '순위.가게이름' 저장할 리스트
    simple_explain = [] # 1~10 index에 1~10위 맛집의 간단한 메뉴 설명 저장할 리스트
    url_list = [] # 1~10 index에 맛집 링크 저장할 리스트
    # 1위 ~10위 식당이름하고, 링크 / 배열에는 검색된 것만큼 저장됨!
    for tag in soup.find_all('a', 'blink'): #[0]은 광고글
        title= tag.select('.btxt') #태그의 class가 btxt인 것 셀렉트
        title_name = title[0].get_text() #title에서 텍스트만 뽑아 저장

        simple = tag.select('.stxt') #태그의 class가 stxt인 것 셀렉트
        simple_name = simple[0].get_text() #simple에서 텍스트만 뽑아 저장

        title_link = tag.get('href') #a 태그에서 href 속성을 이용, 주소를 저장

        rank_list.append(title_name) #rank_list 리스트에 맛집 이름 덧붙임
        simple_explain.append(simple_name) #simple_explain 리스트에 맛집 간단 설명 덧붙임
        url_list.append('https://www.diningcode.com'+title_link) #url_list 리스트에 맛집 링크 덧붙임
    return rank_list, simple_explain, url_list

#여러개의 큰 태그를 고르고 싶을 때 find_all
#find_all로 찾은 큰 덩어리에서 for문과 select 이용, 특정 부분 활용할 수 있음
#select로 고른 대상이 하나일 것 같아도 soup.select('태그명.클래스명')[0] 이렇게 첨자를 꼭 붙여줘야함


# 맛집 상세 정보 
def dining_code_detail(detail_url):
    html = req.get(detail_url).text
    soup = bfs(html, 'html.parser')

    # 식당 대표 이미지
    soup_food_image = soup.select('li.bimg > img')
    if soup_food_image is not None and len(soup_food_image) > 0:
        food_image = soup_food_image[0]['src']
    else:
        food_image = ""
    #notification(food_image)  # 맛집이미지 답변
    #time.sleep(1)

    # 영업시간
    run_hour1 = soup.findAll('p','l-txt')
    run_hour2 = soup.findAll('p', 'r-txt')
    if run_hour1 is not None and len(run_hour1) > 0 and run_hour2 is not None and len(run_hour2) > 0:
        hour_section1 = run_hour1[0].get_text()
        hour_section2 = run_hour2[0].get_text()
        possible_hour = "- 영업시간: " + hour_section1 + " " + hour_section2
        # notification(possible_hour)  # 영업시간 답변
    else:
        possible_hour = ""
    #possible_hour = "- 영업시간: " + soup.select('p.l-txt')[0].text + " " + soup.select('p.r-txt')[0].text

    # 평균 평점
    soup_average_point = soup.select('p.star-point > span.point')
    if soup_average_point is not None and len(soup_average_point) > 0:
        star_point = "- 평균평점: " + soup_average_point[0].text + "(5점 만점)"
        # notification(star_point)
    else:
        star_point = ""
    #average_point = "- 평균평점: " + soup.select('p.star-point > span.point')[0].text + "(5점 만점)"
    #notification(average_point) #평균평점 답변

    # 블로그 후기 url 1개
    soup_blog_review = soup.select('#div_blog > li > a')
    if soup_blog_review is not None and len(soup_blog_review) > 0:
        blog_review = "- 블로그 후기 URL: " + soup_blog_review[0]['href']
    else:
        blog_review = ""
        # notification(blog_review)

    #주소
    soup_map = soup.select('li.locat')
    if soup_map is not None and len(soup_map) > 0:
        map_addr = "- 주소: " + soup_map[0].text
    else:
        map_addr = ""
        # notification(map_addr)
        # 지도 이미지 답변

    #매장 전화번호
    soup_tel = soup.select('li.tel')
    if soup_tel is not None and len(soup_tel) > 0:
        tel_number = "- 전화: " + soup_tel[0].text
    else:
        tel_number = ""

    #관련 해시태그
    soup_tag = soup.select('li.tag')
    if soup_tag is not None and len(soup_tag) > 0:
        hashtag = "- 태그: " + soup_tag[0].text
    else:
        hashtag = ""

    #대표 메뉴, 가격
    soup_menu_cost = soup.select('div.menu-info.short > ul.list > li')
    if soup_menu_cost is not None and len(soup_menu_cost) > 0:
        menu_cost = "- 대표 메뉴 및 가격: " + soup_menu_cost[0].text
    else:
        menu_cost = ""
    # if run_hour1 is not None and len(run_hour1) > 0 and run_hour2 is not None and len(run_hour2) > 0:
    #     menu_cost = "대표 메뉴 및 가격: " + run_hour1[2].get_text() + run_hour2[2].get_text() + "/" + run_hour1[3].get_text() + run_hour2[3].get_text() + "/" + run_hour1[4].get_text() + run_hour2[4].get_text()

    # menu_cost = "대표 메뉴 및 가격: "
    # for tag in soup.find_all('div', 'menu-info.short'):
    #     menu = tag.select('p')
    #     for i in [1,2,3,4,5,6]:
    #         menu_cost += menu[i].text


    dic = {
        "color" : "#CEE3F6",
        "text" :  possible_hour + "\n" + menu_cost + "\n" + star_point + "\n" + blog_review + "\n"+ hashtag + "\n" + tel_number + "\n"+ map_addr + "\n",
        "image_url": food_image
    }
    attachments = [dic]
    notification2(attachments)

    map_image(detail_url)  # 함수 호출
    # notification("------------------------------------------------------------------------------")

    dic = {
        "color": "#FA5858",
        "text": "☞검색된 맛집의 상세한 정보가 알고 싶다면 해당 맛집의 순위를 입력해주세요\nex)'1' -> 1위의 정보가 나옵니다.\n☞맛집을 재검색하시려면 '끝' 이라고 입력해주세요",
        "mrkdwn_in": ["text", "pretext"]
    }
    attachments = [dic]
    notification2(attachments)


# 맛집 지도 이미지 정보
def map_image(detail_url):
    #다이닝 코드 상세 맛집 url에서 위도, 경도 정보 파싱해서 가져오기
    html = req.get(detail_url).text
    soup = bfs(html, 'html.parser')

    soup_lat = soup.select('#hdn_lat') #위도
    soup_lng = soup.select('#hdn_lng') #경도

    if soup_lat is not None and len(soup_lat) > 0 and soup_lng is not None and len(soup_lng) > 0:

        latitude = soup_lat[0]['value']
        longitude = soup_lng[0]['value']

        real_latitude = float(latitude)
        real_longitude = float(longitude)

        #folium 라이브러리 활용, 맛집에 마커된 지도 html파일 생성
        food_location = [real_latitude, real_longitude]
        map = folium.Map(location=food_location, zoom_start=25)
        folium.Marker(food_location, popup='destination').add_to(map)
        map.save('./location.html')
        map

        #selenium 라이브러리 활용, 지도 html파일을 스크린샷캡쳐해서 정적이미지 파일로 생성
        browser = webdriver.Chrome('C:/Users/yurim/Desktop/chromedriver.exe') #크롬드라이버경로넣어줘야함
        browser.get('C:/Users/yurim/Documents/GitHub/capstone-capyou/code/complete_code/location.html') #지도 html경로
        browser.save_screenshot('restaurant_location.png')
        #time.sleep(2)
        #browser.quit() #동적 지도창 닫지 않기 위해서 주석 처리
        #다른 맛집 검색하거나 끝 누르면 html 창 자동으로 사라짐, 그 전에 마음대로 닫으면 오류 발생

        # slackbot 답변으로 위에서 저장된 이미지 파일 답변하기
        map_image_file = {
            'file': ('restaurant_location.png', open('restaurant_location.png', 'rb'), 'png')
        }

        map_image_file_detail = {
            "filename": "restaurant_location.png",
            "token": token,
            "channels": ['#general']
        }
        r = req.post("https://slack.com/api/files.upload", params=map_image_file_detail, files=map_image_file)

    else:
        return

    # with open('restaurant_location.png') as file_content:
    #     sc.api_call(
    #         "files.upload",
    #         params = map_image_file_detail
    #     )
    # slack.chat.post("files.upload", params=map_image_file_detail, files=map_image_file)

#굳이 따지자면 여기부터가 main 역할
if sc.rtm_connect():
    #맨 처음 출력하는 소개 글
    dic = {
        "color": "#01A9DB",
        "title": "맛집 검색 서비스입니다.\n자유로운 형태로 맛집을 검색하세요!\n(1~5위의 맛집이 검색됩니다.)",
        "mrkdwn_in" : ['text', 'pretext']
    }
    attachments = [dic]
    notification2(attachments)
    
    while True:
        receive_data = sc.rtm_read()
        if len( receive_data ):
            keys = list( receive_data[0].keys() )
            if 'type' in keys and 'text' in keys and 'user' in keys:
                print( receive_data[0] )
                message = receive_data[0]['text']
                print(message)
                #title_result:맛집 이름 / simple_result: 맛집 간단한 메뉴설명 / url_list:맛집 상세 URL
                title_result, simple_result, url_list = dining_code(message) #dining_code 함수 호출 후 result에 담기
                print(url_list) # 콘솔에 출력

                ## 맛집 리스트 에러 처리 1)하나도 없거나 2)5개 미만이거나 3)5개 이상이거나
                # 리스트의 length를 구해야 함
                list_len = len(title_result)

                # 리스트의 개수가 0개이면
                if list_len == 0 or list_len == 1: #리스트의 0번째에는 광고글이 담긴다는 것 생각하기
                    notification("검색된 맛집이 없습니다.")
                    break;

                # 리스트의 개수가 5개 미만이면 리스트 개수만큼 출력
                elif 1< list_len < 6:
                    i = 1
                    while i < list_len:
                        dic = {
                            "color" : "#E6E6E6",
                            "title" : title_result[i],
                            "text" : '-'+simple_result[i]
                        }
                        attachments = [dic]
                        notification2(attachments)
                        # notification(title_result[i])
                        # notification('-'+simple_result[i])
                        i += 1

                # 리스트의 개수가 5개 이상이면
                else:
                    for i in [1, 2, 3, 4, 5]:  # index 1~5까지 반복(맛집 1~5위에 해당)
                        dic = {
                            "color": "#E6E6E6",
                            "title": title_result[i],
                            "text": '-' + simple_result[i]
                        }
                        attachments = [dic]
                        notification2(attachments)
                        # notification(title_result[i])  # slack으로 답변해줌
                        # notification('-' + simple_result[i])

                dic = {
                    "color" : "#FA5858",
                    "text" : "☞검색된 맛집의 상세한 정보가 알고 싶다면 해당 맛집의 순위를 입력해주세요\nex)'1' -> 1위의 정보가 나옵니다.\n☞맛집을 재검색하시려면 '끝' 이라고 입력해주세요",
                    "mrkdwn_in": ["text", "pretext"]
                }
                attachments = [dic]
                notification2(attachments)
                # notification("**검색된 맛집의 상세한 정보가 알고 싶다면 해당 맛집의 순위를 입력해주세요 ex)'1' -> 1위의 정보가 나옵니다.")
                # notification("**맛집을 재검색하시려면 '끝' 이라고 입력해주세요")

                # 이미지 답변 테스트
                # notification("https://s3-ap-northeast-1.amazonaws.com/dcreviewsresized/600_400_20180121035724_photo2_0bfc2d5fa8f6.jpg")

                while True:
                    receive_data2 = sc.rtm_read()
                    if len(receive_data2):
                        keys = list(receive_data2[0].keys())
                        if 'type' in keys and 'text' in keys and 'user' in keys:
                            print(receive_data2[0]) #출력 테스트
                            msg = receive_data2[0]['text'] # 입력받은 값 message 변수에 저장

                            if msg == "끝": #끝이라는 메시지가 슬랙에서 입력되면 다른 지역의맛집을 탐색할 수 있도록 break
                                dic = {
                                    "color": "#01A9DB",
                                    "title": "자유로운 형태로 맛집을 검색하세요!\n(1~5위의 맛집이 검색됩니다.)",
                                    "mrkdwn_in": ['text', 'pretext']
                                }
                                attachments = [dic]
                                notification2(attachments)
                                break
                            
                            elif msg =="": #빈 문자열인 경우 다음 반복으로 뛰어넘음
                                continue

                            #'끝'이 아닐 경우 맛집의 상세정보를 알 수 있음
                            else:
                                try:
                                    rank = int(msg) #사용자가 입력한 맛집 순위(문자열)를 정수형으로 변환하여 배열의 인덱스로 사용하기 위해
                                except ValueError:
                                    pass

                            #notification(url_list[rank]) #해당 순위 맛집의 url 답변
                            dic = {
                                "color":"#CEE3F6",
                                "title":title_result[rank] + " 상세정보"
                            }
                            attachments = [dic]
                            notification2(attachments) #'맛집 이름 상세정보'title 출력

                            # notification("------------------------------------------------------------------------------")
                            # notification("###"+title_result[rank]+" 상세정보###")

                            dining_code_detail(url_list[rank]) #맛집 상세 정보 답변하기 위해 함수 호출
                    time.sleep(1)

        time.sleep(1)

else:
    print("connection Failed")










































# import requests
# from slacker import Slacker
# from slackclient import SlackClient
# from konlpy.tag import Okt
# import time
#
# from bs4 import BeautifulSoup
# import urllib.request
# from urllib.parse import quote # quote : url주소에 한글(UTF-8)이 포함되었을 때 아스키 형식으로 바꿔줌
#
# TARGET_URL_BASIC = "http://www.diningcode.com/list.php?"
# TARGET_URL_BEFORE_KEYWORD = 'query='
#
#
#
#
#
#
# def notification(message):  # 사용할 slack 설정
#     token = 'xoxb-445422292193-447426542310-hpnHoRJsiKKn2XA8Ud8USU00'
#     slack = Slacker(token)
#     slack.chat.post_message('#general', message)
#
# slack_token = 'xoxb-445422292193-447426542310-hpnHoRJsiKKn2XA8Ud8USU00'
# sc = SlackClient( slack_token )
#
# def crawl_foodlist(message):
#     keyword = message
#
#     target_URL = TARGET_URL_BASIC + TARGET_URL_BEFORE_KEYWORD + quote(keyword)
#     response = requests.get(target_URL)
#     html = response.text
#     soup = BeautifulSoup(html, 'html.parser')
#
#     #source_code_from_URL = urllib.request.urlopen(target_URL)
#     # soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='UTF-8')
#
#     for food in soup.select('a[class=blink]'):
#         print(food.text)
#
#
#
#
#     #rank_list = []
#     # 1위~10위 식당이름하고 링크
#     #for idx, tag in enumerate(soup.select('div.dc-restaurant-name a'), 1):
#     #    rank_list.append('{}.{}'.format(idx, tag.text) + ' ' + 'http://www.diningcode.com/' + tag['href'])
#     #notification(rank_list)
#     #파이썬 반복문 i를 1로 초기값두고 증가시키면서 반복문 돌리는거 알아보기
#
#
#
#
# if sc.rtm_connect():
#     while True:
#         receive_data = sc.rtm_read()
#
#         if len(receive_data):
#             keys = list(receive_data[0].keys())
#             if 'type' in keys and 'text' in keys and 'user' in keys:
#                 print(receive_data[0])
#                 message = receive_data[0]['text'] #사용자가 입력한 메세지를 message 변수에 받음
#                 #함수 호출
#                 crawl_foodlist(message)
#
#         time.sleep(1)
#
# else :
#     print("connection Failed")