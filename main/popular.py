import datetime
import requests as r
import re
import time
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
cookie = {'over18':'1'}

def modified_requests(url):
    attempts = 10
    while(attempts > 0):
        try:
            request = r.get(url,headers=headers,cookies=cookie)
        except r.HTTPError:
            attempts -= 1
            print('retry')
            time.sleep(10)
            continue
        break
        
    return request

def get_popular_board():
    base_url = 'https://www.ptt.cc/bbs/index.html'
#    request = r.get(base_url,headers=headers)
    request = modified_requests(base_url)
    html = request.text
    bs_class = BeautifulSoup(html,'html.parser')
    result = []
    all_raw_board = bs_class.find_all('div',class_='board-name')
    for raw_board in all_raw_board:
        try:
            link = 'https://www.ptt.cc/bbs/' + raw_board.text + '/index.html'
        except TypeError:
            continue 
        board = raw_board.text
        result.append(board)
    request.close()
    #result 為 dictionary array, eg. result[0]['board'] or result[5]['link']
    return result