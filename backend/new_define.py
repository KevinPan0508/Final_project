import datetime
import requests as r
import re
import time
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
cookie = {'over18':'1'}

session = r.Session()

def modified_requests(url):
    attempts = 10
    while(attempts > 0):
        try:
            request = session.get(url,headers=headers,cookies=cookie)
        except r.HTTPError:
            attempts -= 1
            print('retry')
            time.sleep(10)
            continue
        break
    return request

def get_popular_board():
    base_url = 'https://www.ptt.cc/bbs/index.html'
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
        if(len(result)<=20):
            result.append({'board':board,'link':link})
        else:
            break
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
    print(url)
    return result

def get_previous_page_link(current_page_url):
    #取url數字
    pattern = re.compile(r'\d+')
    url_digit = pattern.findall(current_page_url)
    if(url_digit):
        previous_page_link = current_page_url.replace(url_digit[0],str(int(url_digit[0])-1))
    else:
        request = modified_requests(current_page_url)
        html = request.text
        bs_class = BeautifulSoup(html,'html.parser')
        previous_page_link = 'http://ptt.cc' + bs_class.find_all('a',class_='btn wide')[1]['href']
    return previous_page_link

def get_text(url):
    request = modified_requests(url)
    html = request.text
    bs_class = BeautifulSoup(html,'html.parser')
    return bs_class.text

def compute_target_time(minus):   
    now = datetime.datetime.now()
    offset = datetime.timedelta(days=minus)
    time = now-offset
    return time.strftime('%m/%d')

def get_text_7days(board,type='text'):
    url = 'https://www.ptt.cc/bbs/' + board + '/index.html'
    all_text = []
    only_text = []
    temp = get_title_meta_per_page(url)
    d = 5
    while(1):
        try:
            temp = temp[:-d]
            break
        except IndexError:
            d-=1
            continue
        target_time = compute_target_time(7).lstrip('0')
    while(1):
        for i in range(len(all_text),-1,-1):
            try:
                if(all_text[i]['date'] == target_time):
                    all_text = all_text[:i]
                    if(type=='text+date'):
                        return all_text
                    elif(type=='text'):
                        return only_text
            except IndexError:
                continue
        for i in range(len(temp)):
            date = temp[-1]['date']
            print(temp[-1]['link'])
            text = get_text(temp.pop()['link']).replace('\n','')
            all_text.append({'date':date,'text':text})
            only_text.append(text)
        url = get_previous_page_link(url)
        temp = get_title_meta_per_page(url)

def get_text_by_number(board,type='text'):
    url = 'https://www.ptt.cc/bbs/' + board + '/index.html'
    all_text = []
    only_text = []
    temp = get_title_meta_per_page(url)
    while(1):
        for i in range(len(temp)):
            print(temp[-1]['link'])
            text = get_text(temp.pop()['link']).replace('\n','')
            if(len(only_text)<=280):
                only_text.append(text)
            else:
                break
        if(len(only_text)>=280):
            break    
        url = get_previous_page_link(url)
        temp = get_title_meta_per_page(url)

def get_text_by_day(board,minus,type='text'):
    url = 'https://www.ptt.cc/bbs/' + board + '/index.html'
    all_text = []
    only_text = []
    temp = get_title_meta_per_page(url)
    d = 5
    while(1):
        try:
            temp = temp[:-d]
            break
        except IndexError:
            d-=1
            continue
    target_time = compute_target_time(minus).lstrip('0')
    while(1):
        for i in range(len(all_text),-1,-1):
            try:
                if(all_text[i]['date'] == target_time):
                    all_text = all_text[:i]
                    if(type=='text+date'):
                        return all_text
                    elif(type=='text'):
                        return only_text
            except IndexError:
                continue
        for i in range(len(temp)):
            date = temp[-1]['date']
            print(temp[-1]['link'])
            text = get_text(temp.pop()['link']).replace('\n','')
            all_text.append({'date':date,'text':text})
            only_text.append(text)
        url = get_previous_page_link(url)
        temp = get_title_meta_per_page(url)


def split_text_by_days(list1):
    time = []
    days7,days6,days5,days4,days3,days2,days1 = [],[],[],[],[],[],[]
    for i in range(0,8):
        time.append(compute_target_time(i).lstrip('0')) 
    days7,days6,days5,days4,days3,days2,days1 = time[0:1], time[1:2], time[2:3], time[3:4], time[4:5], time[5:6], time[6:7]
    days7_text = list(filter(lambda x:x['date'] in days7, list1))
    days7_text = list(map(lambda x:x['text'], days7_text))    
    days6_text = list(filter(lambda x:x['date'] in days6, list1))
    days6_text = list(map(lambda x:x['text'], days6_text))    
    days5_text = list(filter(lambda x:x['date'] in days5, list1))
    days5_text = list(map(lambda x:x['text'], days5_text))       
    days4_text = list(filter(lambda x:x['date'] in days4, list1))
    days4_text = list(map(lambda x:x['text'], days4_text))    
    days3_text = list(filter(lambda x:x['date'] in days3, list1))
    days3_text = list(map(lambda x:x['text'], days3_text))   
    days2_text = list(filter(lambda x:x['date'] in days2, list1))
    days2_text = list(map(lambda x:x['text'], days2_text))   
    days1_text = list(filter(lambda x:x['date'] in days1, list1))
    days1_text = list(map(lambda x:x['text'], days1_text))   
    return days7_text,days6_text,days5_text,days4_text,days3_text,days2_text,days1_text




