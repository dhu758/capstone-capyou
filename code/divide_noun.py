# divide_noun.py
# 문장을 받아 명사로 분리/추출하여 -> 크롤링의 키워드 입력값으로 던지는 것이 목표
# 더 해야할 작업
# 1.슬랙봇에서 입력되는 문장을 이 코드로
# 2.여기서 분리한 명사 리스트를 크롤링 코드에 키워드로(크롤링에서 이 리스트의 문자들을 +로 연결해야함)
# -> 이렇게 main으로 따로 만들 것이 아니라 크롤링 코드에 합쳐서 함수로 구현해도 될듯! 그럼 넘겨주기 편리해질 듯 함

import sys
from konlpy.tag import Twitter

def main():
    spliter = Twitter()
    sentence = "문재인의 청년일자리 의견을 알려줘"
    print(spliter.nouns(sentence))


if __name__ == '__main__':
    main()

# def get_tags(text, ntags = 50):
#     spliter = Twitter()
#     # noun에는 'Twitter'객체의 'nouns'메소드에 의해 분리된 명사들이 순환가능한 객체로 저장됨
#     nouns = spliter.nouns(text)
#     return_list = []
#     for n in count.most_common(ntags):
#         temp = {'tags':n}
#         return_list.append(temp)
#         return return_list