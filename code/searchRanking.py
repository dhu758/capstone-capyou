import requests
from bs4 import BeautifulSoup

req = requests.get("http://naver.com") #네이버와 연동
#req =
requests.get("http://datalab.naver.com/keyword/realtimeList.naver? where=main")
html = req.text #naver에서 소스 받아오기

#BeautifulSoup으로 html 소스를 파이썬 객체로 변경 가능함
# 첫 인자에는 html 소스, 두 번째 인자에는 이용할 파서를 설정
# 파이썬 내장 함수 : html.parser

soup = BeautifulSoup(html, 'html.parser')
sillsigan = soup.select('div.ah_roll.PM_CL_realtimeKeyword_rolling_base > div > ul > li')
#실시간 검색어 부분 카피 select

b = []
for sill in sillsigan:
    b.append(sill.text) #tag내의 문자열을 b 리스트에 추가

k=1;
list_sillsigan = []
print("="*30 + '\n' + ' '*7 + "NAVER RANK LIST\n" + '='*30)

for i in b:
    if k>9 :
        list_sillsigan.append(i[5: -2])
    else :
        list_sillsigan.append(i[4: -2])
    k+=1

for s, list in enumerate(list_sillsigan):
    print("%d위 "%(s+1)+list)