import folium

my_location = [37.498310,127.025232]
map = folium.Map(location=my_location, zoom_start=25)
folium.Marker(my_location, popup='destination').add_to(map)
map.save('./index.html')
map

# notification('capture_map.png')


    # #파일 업로드 추가
    # with open('capture_map.png') as file_content:
    #     sc.api_call(
    #         "files.upload",
    #         channels="#general",
    #         file=file_content,
    #         title="Test"
    #     )
    # #추가끝




# import urllib.request
#
# client_id = "A9sdyWlqliQExpHhU_R_"
# client_secret = "9Q9bb9Js9D"
#
# url_base = "https://openapi.naver.com/v1/map/staticmap.bin"
# query = "?query="
# detail = "center=127.1946802,37.553507&level=12&w=500&h=500&maptype=default&markers=127.1946802,37.553507"
#
# url = url_base+query+detail
#
# request = urllib.request.Request(url)
# request.add_header("X-Naver-Client-Id",client_id)
# request.add_header("X-Naver-Client-Secret",client_secret)
#
# response = urllib.request.urlopen(request)
# rescode = response.getcode()
# if(rescode == 200):
#     response_body = response.read()
#     print(response_body.decode('utf-8'))
#     notification(response_body)
# else:
#     print("Error code:"+rescode)

    # 지도 api 사용
    # map_url = "https://openapi.naver.com/v1/map/staticmap.bin?clientId=A9sdyWlqliQExpHhU_R_&url=http://sample.co.kr&crs=EPSG:4326&center=127.025232,37.498310&level=1&w=320&h=320&baselayer=default&format=jpeg&markers=127.025232,37.498310"
    # notification(example)
    # map = folium.Map(location=[127.1946802,37.553507], zoom_start=12)
    # folium.Marker([127.1946802,37.553507], popup='index').add_to(map)
    # map.save('./index.html')
    # notification('https://ssl.pstatic.net/static/maps/mantle/1x/pattern_1.png')

