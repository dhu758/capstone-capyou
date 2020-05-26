from slacker import Slacker
from slackclient import SlackClient
from konlpy.tag import Okt
import time

#crawling.py
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote # quote : url주소에 한글(UTF-8)이 포함되었을 때 아스키 형식으로 바꿔줌

TARGET_URL_BEFORE_PAGE_NUM = "http://news.donga.com/search?p="
TARGET_URL_BEFORE_KEYWORD = '&query='
TARGET_URL_REST = '&check_news=1&more=1&sorting=3&search_date=1&v1=&v2=&range=2'
# 동아일보 url 주소를 참고한 것
# more=1 기사 검색 결과를 더보기를 누른 상태로 만들어줌
# sorting=3 '정확도' 기준 기사 정렬
# range=2 제목으로 범위 한정 //range=1은 전체
# query='던져줄 키워드'

def notification(message):  # 사용할 slack 설정
    token = 'xoxb-445422292193-447426542310-hpnHoRJsiKKn2XA8Ud8USU00'
    slack = Slacker(token)
    slack.chat.post_message('#general', message)

slack_token = 'xoxb-445422292193-447426542310-hpnHoRJsiKKn2XA8Ud8USU00'
sc = SlackClient( slack_token )

def get_link_from_news_title(page_num, URL, output_file): # 페이지 URL 만들고, 기사 URL을 찾아 본문 내용 추출
    for i in range(page_num):
        current_page_num = 1+i*15         # 페이지당 15개의 게시물
        position = URL.index('=')        # URL 처음 = 오는 위치 반환(URL에 몇페이지 인지 추가하기 위해)
        URL_with_page_num = URL[: position+1] + str(current_page_num) + URL[position+1 :]        # 페이지가 있는 URL을 재구성
        source_code_from_URL=urllib.request.urlopen(URL_with_page_num)        # 재구성한 URL을 request로 호출
        soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='UTF-8')       # BeautifulSoup로 변환, 기사 분석 후 추출하기 위해

        for title in soup.find_all('p', 'tit'):
            # tit_res = soup.find_all('p', 'tit')
            # for n in tit_res:
            #     print(n.get_text())
            #이렇게 하면 다른 기사들 제목까지 다나옴 ㅠ

            title_link = title.select('a')
            article_URL = title_link[0]['href']
            print(article_URL) #기사 링크 콘솔에 출력!
            title_name = title_link[0].get_text() #기사 제목 title_name 변수에 담기
            print(title_name) #기사 제목 콘솔에 출력!
            notification("기사 제목: "+ title_name) #슬랙에 기사 제목 전달
            notification("기사 URL: "+article_URL) # 슬랙에 기사 링크 전달

            break
            # get_text(article_URL, output_file)
            # 본문 기사가 담긴 URL을 찾기 위해
        break

# def get_text(URL, output_file):
#     source_code_from_url = urllib.request.urlopen(URL) # urllib로 기사 페이지 요청받음
#     soup = BeautifulSoup(source_code_from_url, 'lxml', from_encoding='UTF-8') # BeautifulSoup로 페이지를 분석하기 위해 soup변수로 할당
#     content_of_article = soup.select('div.article_txt') # 기사의 본문 내용을 추출
#     for item in content_of_article:
#         string_item = str(item.find_all(text=True))
#         output_file.write(string_item) # 기사에 텍스트가 있다면 파일에 씀

# main 함수
def countnouns(result):
    keyword = result # 검색하고자 하는 단어(공백 포함시 + 붙이는 거 맞나...)
    print(result)
    page_num = 1        # 가져올 페이지 숫자
    output_file_name = "crawling_output.txt"         # 기사 url 크롤링 한 것 저장할 파일
    target_URL = TARGET_URL_BEFORE_PAGE_NUM + TARGET_URL_BEFORE_KEYWORD + quote(keyword) + TARGET_URL_REST
    output_file = open(output_file_name, 'w', -1, "utf-8")
    # 함수를 통해서 page 갯수 만큼 크롤링
    get_link_from_news_title(page_num, target_URL, output_file)
    output_file.close()

if sc.rtm_connect(): # 명사 분리하여 result에 값 넣기
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

                    #print(i)
                    notification('단어추출 : ' + i)
                    if i == '대해' or i == '공약': # 대해, 공약 등의 명사가 추출된 경우 검색어에서 제외하기 위해
                        continue

                    print(i)
                    # notification('단어추출 : ' + i)

                    result = result + i + "+"
                #print(result)
                countnouns(result)
        time.sleep(1)

else:
    print("connection Failed")



