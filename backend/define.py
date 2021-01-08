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
        result.append({'board':board,'link':link})
    request.close()
    #result 為 dictionary array, eg. result[0]['board'] or result[5]['link']
    return result

def get_title_meta_per_page(board_page_url):
    url = board_page_url
    #通過18歲驗證
    request = modified_requests(url)

    html = request.text
    bs_class = BeautifulSoup(html,'html.parser')
    result = []
    all_raw_data = bs_class.find_all('div',class_='r-ent')
    for raw_data in all_raw_data:
        
        try:
            link = 'https://www.ptt.cc' + raw_data.find('div',class_='title').find('a')['href']
        except TypeError:
            continue
        date = raw_data.find('div',class_='date').text.lstrip()
        result.append({'link':link,'date':date})
    request.close()
    print(url)
    return result

def get_previous_page_link(current_page_url):
    #取url數字
    pattern = re.compile(r'\d+')
    url_digit = pattern.findall(current_page_url)
    if(url_digit):
        previous_page_link = current_page_url.replace(url_digit[0],str(int(url_digit[0])-1))
    else:
        '''
        cookie = {'over18':'1'}
        request = r.get(current_page_url,cookies=cookie,headers=headers)
        '''
        request = modified_requests(current_page_url)
        html = request.text
        bs_class = BeautifulSoup(html,'html.parser')
        previous_page_link = 'http://ptt.cc' + bs_class.find_all('a',class_='btn wide')[1]['href']
        request.close()
    return previous_page_link




def get_text(url):
    '''
    cookie = {'over18':'1'}
    request = r.get(url,cookies=cookie,headers=headers)
    '''
    request = modified_requests(url)
    html = request.text
    bs_class = BeautifulSoup(html,'html.parser')
    request.close()
    return bs_class.text


def compute_target_time(board):   
    now = datetime.datetime.now()
    if(board=='Gossiping'):
        offset = datetime.timedelta(days=1)
    else:
        offset = datetime.timedelta(days=7)
    time = now-offset
    return time.strftime('%m/%d')

    

def get_7_days_text(board):
    url = 'https://www.ptt.cc/bbs/' + board + '/index.html'
    all_text = []
    temp = get_title_meta_per_page(url)
    d = 5
    while(1):
        try:
            temp = temp[:-d]
            break
        except IndexError:
            d-=1
            continue
    target_time = compute_target_time(board).lstrip('0')
    
    while(1):
        for i in range(len(all_text),-1,-1):
            try:
                if(all_text[i]['date'] == target_time):
                    all_text = all_text[:i]
                    return all_text
            except IndexError:
                continue
        for i in range(len(temp)):
            date = temp[-1]['date']
            print(temp[-1]['link'])
            text = get_text(temp.pop()['link']).replace('\n','')
            all_text.append({'date':date,'text':text})
        url = get_previous_page_link(url)
        temp = get_title_meta_per_page(url)



    